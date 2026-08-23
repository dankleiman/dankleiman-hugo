---
title: "Beware Inherited Constraints"
date: 2026-08-23
description: "A database cost project that started as 'move data to cheaper storage' ended by eliminating the biggest dependency entirely, once the team stopped treating an existing implementation's requirements as fixed and started asking what outcome each one actually served."
summary: "A database cost project that started as 'move data to cheaper storage' ended by eliminating the biggest dependency entirely, once the team stopped treating an existing implementation's requirements as fixed and started asking what outcome each one actually served."
tags: ["software engineering", "software architecture", "technical leadership"]
categories: ["code"]
---

We owned the most expensive database at the company and we needed to drive the cost down. For a (mostly) append-only event log, the obvious choices were "keep less data" or "put the data somewhere cheaper." But we were serving dozens of callers and we knew that any changes to retention or performance would potentially degrade or even break their services.

Moving petabytes of data into a new system would be expensive, so we needed a way to test possible solutions early and rule out anything that would impact throughput and response latency too much.

We introduced a setting to add artificial latency to our response times. We slowly dialed up the added latency, and together with each team using our service, we watched how far we could go before negatively impacting their system. We hoped that if callers could tolerate enough additional latency, we could validate cheaper, slower storage as an option. Unfortunately, most services degraded well before we could hit the right target.

## Stepping Back from a Failed Test

The failed latency test was a low point, but it forced us to step back from the storage designs we had been pursuing.

We looked at call distribution and found that one service made up 80% of the demand.

Initially we said "this database costs too much." But if one service dominates usage a better question is "does what that service gets from this database justify such an expensive dependency?"

So we dug into what this dominant caller — a workflow engine — was actually doing with our data and why.

## Crossing System Boundaries

The workflow engine was several years old and its dependency on our data worked just fine from their perspective. Nobody had much incentive to revisit the interaction pattern.

Fortunately, there were rich execution logs, so we could see what the workflows were actually doing.

Another 80/20 pattern emerged: close to 80% of the workflow execution steps that relied on our data were effectively asking "has this person been through this workflow before?" When the execution code was written, checking the event history that we provided was a perfectly reasonable way to get the answer. Back then we didn't have a data retention problem, either. The systems were brand new.

Years later, that check was running at high volume against event histories that stretched back almost a decade for our oldest customers. A once-reasonable lookup had grown into a very expensive way to answer a simple question.

We brought this back to the workflow team and they realized they already had execution state inside their own system that could efficiently answer this question.

We had removed the biggest reason our largest caller needed the dependency with a conversation, not a system migration.

That changed how we approached the rest of the callers. Instead of assuming each access pattern had to survive, we asked what outcome it supported and whether that outcome justified the dependency. Some callers:

- only needed short windows of history
- could tolerate the latency of cold storage
- could use an offline alternative
- could get the information somewhere else
- were relying on legacy behavior nobody actually needed anymore

## Implementation vs Outcome-Oriented Thinking

Sam Lambert recently [tweeted](https://x.com/samlambert/status/2089891550390263891), "some engineers are struggling to adapt to using agents because they are not used to being outcome oriented." I love this framing, but I don't think it's strictly about agents or AI. At the beginning of this project, we fell into implementation-oriented thinking instead of being outcome oriented too.

Implementation-oriented reasoning looks like:

> We need to cut costs and this data is too expensive to maintain online for all time.  
> → Let's move it offline to save money.  
> → Cold storage has higher latency.  
> → Our biggest caller requires low latency.  
> → What architecture can satisfy that?  
> → What about this access pattern?  
> → What about that ownership constraint?  
> → What about this legacy behavior?

We locked in requirements upfront based on current performance metrics. The list of requirements kept growing as we added new edge cases, taking each one at face value. That left us trying to serve the same all-time data cheaper and faster, prototyping one new storage engine after another with the same requirements.

Outcome-oriented reasoning is more like:

> What are customers actually trying to accomplish?  
> → What usage corresponds to each outcome?  
> → Which outcomes dominate?  
> → Which existing behaviors are actually necessary?  
> → Which dependencies can disappear?  
> → What remains after we remove them?

Then we can evaluate implementations against a much smaller problem, because we've narrowed in on what's important before exploring what's possible.

Instead of taking every access pattern, latency expectation, and legacy behavior of the current implementation as a hard requirement, we started linking each constraint to an outcome. Some of them turned out to be "inherited constraints": requirements that come from the way an intermediate system currently works, not from an outcome the end user ultimately needs.

We initially thought the workflow engine needed low-latency access to ten years of event data. Why? Because it needed to see if someone had ever gone through this workflow before. Did answering that question need ten years of low-latency event data? No. The latency/retention constraint was inherited from the intermediate implementation.

Ask yourself: if you ripped out this intermediate implementation entirely, would the constraint still have to be true to achieve the outcome? If not, it's probably inherited.

If you can't justify a constraint independently of the implementation that introduced it, you should ignore it.

## Why Implementation-Oriented Thinking is So Seductive

Implementation constraints are appealing because they're concrete.

- "This caller sends 50K QPS."
- "This API needs 100ms latency."
- "This team owns this service."
- "This storage tier has this retention period."

You can measure them. Benchmark them. Diagram them. They scope an engineering problem you can immediately get to work on.

As you work across systems, you accumulate inherited constraints for exactly this reason: teams tend to hand each other the requirements that their current implementation exposes. QPS, latency, and retention are all concrete and easy to specify.

With every handoff it gets harder to tell which constraints belong to the problem and which were introduced by the systems in between.

## A New Steel Thread

When a problem is ambiguous, I often hear "find the steel thread": get one narrow path working end-to-end, then build out from there.

But this experience changed what I think that thread should represent.

Don't confuse the happy path implementation with the direct path to the most important outcome.

At first we thought "serving historical data from cheaper storage" was the steel thread. If we had built that path end-to-end, we would have learned a lot about storage engines, migrations, latency, and cost. But the more important outcome was to trace "prevent customers from going through this workflow twice."

Following that thread end-to-end crossed several system boundaries and eventually eliminated the storage dependency entirely.

"Prevent someone from going through the workflow twice" would never have appeared on a list of ways to reduce the database costs. But once we stopped letting the current implementation define the problem, following that outcome showed us how to remove the biggest source of demand entirely.
