+++
date = "2019-10-20T07:43:13-04:00"
title = "SQL Quick Tip: Deduping Data with Row Number"
description = ""
categories = ['Code', 'SQL', 'Quick Tip']
+++

Sometimes when you are inspecting data, you come across duplicates that shouldn't exist.

Here's a an easy way to remove duplicate rows using the `ROW_NUMBER` function.

<!-- more -->

In a previous post about using [`ROW_NUMBER` to find the latest record for each member in a group](/2019/10/12/sql-quick-tip-find-the-latest-record-for-each-member-of-a-group/), I set up some sample data with this statement:

```
CREATE TABLE metrics AS (
  SELECT
    date,
    CASE WHEN n > random() * 2 and n < random() * 4 THEN 'A'
    WHEN n > random() * 2 and n < random() * 4 THEN 'B'
    WHEN n > random() * 4 and n < random() * 6 THEN 'C'
    WHEN n > random() * 6 and n < random() * 8 THEN 'D'
    WHEN n > random() * 8 and n < random() * 10 THEN 'E'
    ELSE 'F' END as metric,
    round(random() * 1000) as value
  FROM
    generate_series(1,11,1) as n
  JOIN (
    SELECT
    day + interval '1 day' * round(random()*100) as date
    FROM generate_series('2019-01-01', '2019-01-31', interval '1 day') day
  ) d
  ON true
);
```

While that statement is a great way to get a bunch of random sample data to play with, there is no guarantee that the values or the dates will be unique. In fact, there were several entries for the same metric on the same date:

```
SELECT
  metric,
  date,
  value
FROM
  metrics
WHERE metric = 'A' AND date > '2019-04-01'
ORDER BY date DESC, rn;

 metric |          date          | value 
--------+------------------------+-------
 A      | 2019-04-30 00:00:00-04 |   889 
 A      | 2019-04-30 00:00:00-04 |   891 
 A      | 2019-04-13 00:00:00-04 |   156 
 A      | 2019-04-10 00:00:00-04 |   274 
 A      | 2019-04-02 00:00:00-04 |   812 
 A      | 2019-04-02 00:00:00-04 |   303 
 A      | 2019-04-02 00:00:00-04 |   786 
(7 rows)
```

## Use Row Number to Count Duplicates

With a small set like our example above, you can see that 4/30/2019 has two entries, and 4/2/2019 has three, but in a larger set it becomes harder to detect.

If you want to systematically remove the duplicates, it becomes the same class of problem as the "latest record per member in a group" problem we explored in [the other post](/2019/10/12/sql-quick-tip-find-the-latest-record-for-each-member-of-a-group/).

We can use `ROW_NUMBER` to do the detection for us like this:

```
SELECT
  metric,
  date,
  value,
  ROW_NUMBER() OVER(PARTITION BY metric, date) AS rn
FROM
  metrics
WHERE metric = 'A' AND date > '2019-04-01'
ORDER BY date DESC, rn;

 metric |          date          | value | rn 
--------+------------------------+-------+----
 A      | 2019-04-30 00:00:00-04 |   889 |  1
 A      | 2019-04-30 00:00:00-04 |   891 |  2
 A      | 2019-04-13 00:00:00-04 |   156 |  1
 A      | 2019-04-10 00:00:00-04 |   274 |  1
 A      | 2019-04-02 00:00:00-04 |   812 |  1
 A      | 2019-04-02 00:00:00-04 |   303 |  2
 A      | 2019-04-02 00:00:00-04 |   786 |  3
(7 rows)
```

Notice how we set the partition: `ROW_NUMBER() OVER(PARTITION BY metric, date)`

By partitioning on the duplicate columns, metric and date, we can now count the number of duplicates in each set. More importantly, as we'll see below, we now have a way to systematically access one of each of the duplicate sets.

Now, if the source of the duplication was copying the same exact rows into the table more than once, we would probably have to add the value column to the partition as well. We only need to use metric and date here because of the way the data was generated, but the principle is the same: **build your partition by adding each column you need to dedupe on**.

## Choose One of Each Duplicate Set

We use the same principle to get our deduped set as we did to take the "latest" value, put the `ROW_NUMBER` query in a sub-query, then filter for `rn=1` in your outer query, leaving only one record for each duplicated set of rows:

```
SELECT
  metric,
  date,
  value
FROM (
  SELECT
    metric,
    date,
    value,
    ROW_NUMBER() OVER(PARTITION BY metric, date) AS rn
  FROM
    metrics
  WHERE metric = 'A' AND date > '2019-04-01'
) m
WHERE rn = 1
ORDER BY date DESC;

 metric |          date          | value 
--------+------------------------+-------
 A      | 2019-04-30 00:00:00-04 |   889
 A      | 2019-04-13 00:00:00-04 |   156
 A      | 2019-04-10 00:00:00-04 |   274
 A      | 2019-04-02 00:00:00-04 |   812
(4 rows)
```

You can build off this concept in a bunch of different ways, depending on how your data is structured.

For example, we don't actually have an opinion about which value is correct in this case, so we ignored the value column.

You might have a `created_at` timestamp on each record that signifies the most recently created record should be used. In that case, include `ORDER BY created_at DESC` to the `OVER` statement to make sure you select the correct duplicate value.

This strategy for deduping data can come in handy as you're exploring new tables or when you actually need to find, debug, and correct data transformations. Hope it helps! 