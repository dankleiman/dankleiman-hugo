---
title: "Bounded Windows for Outlier Detection"
date: 2026-09-06
description: "Reusing the bounded-window measurement pattern from an adaptive concurrency controller to detect query outliers — except answering 'is this unusual relative to normal?' needed a lot more state than reacting to the present moment did."
summary: "Reusing the bounded-window measurement pattern from an adaptive concurrency controller to detect query outliers — except answering 'is this unusual relative to normal?' needed a lot more state than reacting to the present moment did."
tags: ["software engineering", "software architecture"]
categories: ["code"]
---

After migrating an old Rails app to PlanetScale, I was poking around in Query Insights and the definition of [notable queries](https://planetscale.com/docs/vitess/monitoring/query-insights#notable-queries) caught my eye. Insights captures any query "that took longer than 1s, read more than 10,000 rows, or produced an error."

When we were building [concurrency control in front of our ClickHouse cluster at Klaviyo](https://klaviyo.tech/adaptive-concurrency-control-for-mixed-analytical-workloads-51350439aeec), we also started with static limits. The project got much more interesting when we tried to make those limits adaptive, moving the concurrency limit up or down based on how much capacity the downstream systems actually had at any given moment.

Seeing the "notable query" thresholds made me wonder if the same idea could apply here. Could a query be notable because it was an outlier against a relative, changing latency baseline rather than because it crossed a fixed threshold?

Of course, one option is to capture every query, ship the executions somewhere persistent, and analyze the distribution of latencies later. That is a perfectly reasonable design if you can export the query stream efficiently.

But I love the bounded windows we used in the adaptive control design. They gave us an inexpensive way to observe traffic and react to changes close to where the traffic was actually being served. So I started playing with reusing that pattern to dynamically detect outliers here too.

## The Window We Already Had

The concurrency controller measured the end-to-end latency of our analytical queries. Sometimes these were short-range aggregate counts and sums that would take 10 ms. Other times they were complex reporting queries that would take several hundred milliseconds or more than a second. The system was serving a mix of both, but we wanted to serve that mix without creating contention or unbounded queuing.

The bounded windows accumulated a small number of round-trip request latencies, including initial server processing, query execution in ClickHouse, and results handling on the way back out.

Each window closed after either N observations or T seconds. When a window closed, we calculated its p99 latency. Depending on the result, the controller could lower the current limit or slowly raise it.

The concurrency limit was available on the request path. When new work arrived, the server compared the current limit with the number of in-flight requests and decided whether to admit more work or reject it. The idea was to shed load before the system entered an overload cycle. Accepting more requests created more queueing, which increased latency and kept work in flight longer, creating even more queueing, until callers experienced extended waves of timeouts.

For that job, a small local window worked great. We cared about what the system was doing *right now*. The observations from a single window told us enough to make an adjustment. After the adjustment, we could throw the window away and start over with fresh measurements.

## A Local p99 Was Not Enough

My first instinct was to reuse essentially the same mechanism to detect query outliers. Collect query latencies. Close the window after N observations or T seconds. Calculate the p99. Any query with latency above that point is "notable."

But taking a single window reading didn't measure the right thing in this case.

For concurrency control, locality was useful. A latency spike right now was the right signal to reduce the amount of work entering the system. For outlier detection, I needed observations over a longer period of time.

Imagine a small observation window during a temporary burst where the whole database slows down. The local p99 will faithfully describe that window, but says very little about whether those executions are unusual relative to the system's normal behavior.

The small window of observations that made the concurrency controller so cheap was too small to be a useful baseline, so I needed a way to keep more history without storing all of the raw query executions.

## Keep the Distribution

That question led me into streaming sketches, and eventually to [t-digest](https://dataorigami.net/2015/03/19/Percentile-and-Quantile-Estimation-of-Big-Data-The-t-Digest.html).

Instead of retaining every latency value, each query can update a compact summary of the distribution. The sketch gives useful percentile estimates without requiring a giant array of all the observations that produced them.

In the window, the update is tiny:

```python
def observe(self, event: QueryEvent):
    self.sketch.update(event.duration_ms)
    self._maybe_record_event(event)
```

Every execution updates the distribution. `_maybe_record_event` can be much more selective about which executions survive the window with their full details intact.

Sketches also have a really cool property: they can be merged.

In the execution path, the observation loop updates a small t-digest for the current window. Once that window closes, a background processor picks it up and merges its sketch into longer-lived history. In a production version, that might mean keeping hourly sketches and building something approximating a rolling 24-hour latency distribution.

That solved the history problem, but it introduced another one.

## Keep the Query

A latency sketch can tell us the p99, but it does not record the query that exceeds it. A "notable query" needs its execution details, fingerprint, and whatever other metadata will help someone understand why it was unusual.

To capture the details, I added a second bounded data structure: a min-heap containing the K slowest query executions seen in the current window.

```python
if event.fingerprint in self._fingerprints:
    return

if len(self.queries) < MAX_SLOW_QUERIES:
    heapq.heappush(self.queries, event)
    self._fingerprints.add(event.fingerprint)
elif event > self.queries[0]:
    evicted = heapq.heapreplace(self.queries, event)
    self._fingerprints.remove(evicted.fingerprint)
    self._fingerprints.add(event.fingerprint)
```

Until the heap contains K queries, a new candidate can simply be added. Once it is full, the root is the fastest query among the K slow queries currently being tracked.

For each new execution, the question becomes: is this slower than the fastest candidate currently being tracked?

If it is, the new query replaces that candidate in the heap. If it is not, the detailed event can be discarded.

Importantly, even for skipped queries, the latency has already been added to the t-digest. Every execution contributes to the latency distribution, but only a bounded number are retained in full detail.

For this prototype, once a fingerprint has been captured in the window, I ignore later executions with the same fingerprint. I didn't want one pathological query to consume every slot in the heap. That means that a later execution of the same query could be even slower, but I'm trading that for per-window deduplication to try to capture a wider range of queries.

The K slowest queries in one small window are not necessarily outliers against the longer historical distribution. Most windows probably contain no "notable" queries at all.

On the other hand, a query that is truly extreme relative to the historical distribution is likely to appear among the slowest executions in its local window. The values of K and the window size determine how much gets captured, so this is still a lossy selection process. A candidate can be crowded out if enough even-slower executions occur in the same window.

If the same fingerprint repeatedly clears the outlier filter, then frequency becomes useful information. One outlier execution might be noise, but a query that keeps appearing in the outlier stream is much more likely to deserve attention.

## Keep It Out of the Hot Path

At this point the window is doing two small pieces of work for every completed query:

1. update the t-digest
2. see if the query qualifies for the Top-K heap

PlanetScale describes [how its Postgres extension](https://planetscale.com/blog/behind-the-scenes-how-traffic-control-works) hooks into query execution for Traffic Control before and after it runs. I wanted to model this outlier detection process the same way, which meant that the work per query had to stay extremely small.

When a window reaches its observation limit or deadline, the execution-path code closes it and hands it to a queue. A new window can start accepting observations immediately.

The queue is bounded too:

```python
def put(self, window: Window):
    try:
        self._window_queue.put_nowait(window)
    except Full:
        try:
            self._window_queue.get_nowait()
        except Empty:
            pass

        self._window_queue.put_nowait(window)
```

If the background processor cannot keep up, the queue drops the oldest pending window rather than letting unprocessed windows consume memory indefinitely or make query execution wait for the processing pipeline.

On the other side of that queue boundary, the processor can wait for completed windows and do the work that's too expensive to be in the execution path.

The ordering in the processor is small but important:

```python
def process(self, window: Window):
    self._track_sketch_history()
    self._publish_queries(window.queries)
    self._update_sketches(window.sketch)
```

First, it updates the bookkeeping around the historical time range. Then it compares this window's candidates against the existing baseline. Only afterward does it merge this window's t-digest into that baseline. The window being evaluated doesn't impact the threshold during evaluation.

This is also where network-bound publishing can happen. Once a candidate passes the historical percentile filter, the processor can send it to ClickHouse, another analytical store, or whatever system is responsible for presenting and ranking notable queries.

The full [Python prototype](https://gist.github.com/dankleiman/92e056a792ef232695c5e9a35ae0c709) is intentionally much simpler than a real Postgres implementation. I wanted the code to focus on the state boundaries rather than Postgres extension mechanics: bounded measurement in the query execution path; historical state management, candidate evaluation, and publishing in a separate background process.

## Bounded Memory, Meaningful Signal

I started this experiment wondering whether I could replace a static query threshold with something adaptive.

What I ended up reusing from the ClickHouse concurrency controller wasn't the control algorithm. It was the shape of the measurement system around it.

- Collect cheap observations close to the work.
- Bound the amount of state you retain.
- Close a window and move expensive decisions somewhere else.
- Be explicit about what information can be thrown away to protect performance.

The query version needed more state than the original controller because "what is happening right now?" and "what is unusual relative to normal?" are different questions.

The t-digest let me keep the distribution without keeping every raw observation. The heap let me keep a small amount of potentially valuable raw data without keeping every execution.

Finally, the bounded queue let me move the expensive work away from query execution without creating unbounded backpressure.

The same trade-off kept showing up throughout the design: keep memory and hot path work bounded without throwing away the signal that makes the later decision useful.
