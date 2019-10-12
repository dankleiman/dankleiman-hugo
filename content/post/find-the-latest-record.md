+++
title = "SQL Quick Tip: Find the Latest Record for Each Member of a Group"
date = "2019-10-12T07:30:37-04:00"
categories = ['Code', 'SQL', 'Quick Tip']
+++

In this post, we're going to look at a techinque for finding the lastest full record for each member of a group.

Now, it might not be obvious why this is an annoying problem, but I see people back into having this problem from two different directions.

First, you know how to find the `MAX` date for each member in a group:

```

 metric |     latest_metric      
--------+------------------------
 A      | 2019-04-30 00:00:00-04
 B      | 2019-05-08 00:00:00-04
 C      | 2019-05-08 00:00:00-04
 D      | 2019-05-08 00:00:00-04
 E      | 2019-05-08 00:00:00-04
 F      | 2019-05-08 00:00:00-04
(6 rows)

```

But you need additional column data from the same row as that most recent date.

Or...

You found the whole record for one member in the set:

```

 metric |          date          | value 
--------+------------------------+-------
 A      | 2019-04-30 00:00:00-04 |   889
(1 row)

```

But you need to do the same thing for all the metrics too.

To solve this kind of problem, we can use the `ROW_NUMBER` function to sort our data and reference it as a sorted sub-sets.

Let's break down the pieces that get us to a `ROW_NUMBER` solution.

<!-- more -->

Here is our metrics table:

```
                       Table "public.metrics"
 Column |           Type           | Collation | Nullable | Default 
--------+--------------------------+-----------+----------+---------
 date   | timestamp with time zone |           |          | 
 metric | text                     |           |          | 
 value  | double precision         |           |          | 

```

Start by finding the most recent date for each metric:

```

SELECT
  metric,
  max(date) as latest_metric
FROM
  metrics
GROUP BY 1
ORDER BY 1;

 metric |     latest_metric      
--------+------------------------
 A      | 2019-04-30 00:00:00-04
 B      | 2019-05-08 00:00:00-04
 C      | 2019-05-08 00:00:00-04
 D      | 2019-05-08 00:00:00-04
 E      | 2019-05-08 00:00:00-04
 F      | 2019-05-08 00:00:00-04
(6 rows)

```

Again, this gets us the latest date for each metric, but we don't really have access to the _row_ this data is from. That's what we need if we want to pull additional column values. 

If you only have to answer the question for a single metric, it's easy:

```

SELECT
  metric,
  date,
  value
FROM
  metrics
WHERE metric = 'A'
ORDER BY date DESC
LIMIT 1;

 metric |          date          | value 
--------+------------------------+-------
 A      | 2019-04-30 00:00:00-04 |   889
(1 row)

```

If this is code that lives inside an application that is just looking up the latest data for a specific metric, you're fine with the `ORDER BY` and `LIMIT` solution. But any time you need to jump from a solution that works for one member of the group to all members of the group, you need a **window-based solution** to do it in a single query.

## Finding Records,  Not Just Values

In SQL, window functions allow you to perform operations over subsets of rows by defining a window on the rows. `ROW_NUMBER` is a special window function that will number the rows inside your window.

So, if we take all the metric 'A' rows and add a `ROW_NUMBER` column:

```

SELECT
  metric,
  date,
  value,
  ROW_NUMBER() OVER(PARTITION BY metric ORDER BY date DESC) AS rn
FROM
  metrics
WHERE metric = 'A'
ORDER BY date DESC;

``` 

The numbered rows look like this:

```

 metric |          date          | value | rn 
--------+------------------------+-------+----
 A      | 2019-04-30 00:00:00-04 |   889 |  1
 A      | 2019-04-13 00:00:00-04 |   156 |  2
 A      | 2019-04-10 00:00:00-04 |   274 |  3
 A      | 2019-04-02 00:00:00-04 |   812 |  4
 A      | 2019-03-31 00:00:00-04 |   904 |  5
 A      | 2019-03-29 00:00:00-04 |   611 |  6
 A      | 2019-03-27 00:00:00-04 |   761 |  7
 A      | 2019-03-23 00:00:00-04 |   209 |  8
 A      | 2019-03-06 00:00:00-05 |   231 |  9
 A      | 2019-03-04 00:00:00-05 |    82 | 10
 A      | 2019-02-27 00:00:00-05 |   138 | 11
 A      | 2019-02-25 00:00:00-05 |   537 | 12
 A      | 2019-02-19 00:00:00-05 |   228 | 13
 A      | 2019-02-12 00:00:00-05 |   581 | 14
 A      | 2019-02-11 00:00:00-05 |   657 | 15
 A      | 2019-02-10 00:00:00-05 |     9 | 16
 A      | 2019-02-05 00:00:00-05 |   965 | 17
 A      | 2019-02-04 00:00:00-05 |   826 | 18
 A      | 2019-01-31 00:00:00-05 |   878 | 19
 A      | 2019-01-28 00:00:00-05 |   729 | 20
 A      | 2019-01-26 00:00:00-05 |   168 | 21
 A      | 2019-01-22 00:00:00-05 |   797 | 22
 A      | 2019-01-18 00:00:00-05 |   618 | 23
(23 rows)

```

Without the `WHERE metric = 'A'` filter, you can see that the window function repeats the numbering for each metric:

```

 metric |          date          | value | rn 
--------+------------------------+-------+----
 A      | 2019-04-30 00:00:00-04 |   889 |  1
 A      | 2019-04-13 00:00:00-04 |   156 |  2
 A      | 2019-04-10 00:00:00-04 |   274 |  3
 B      | 2019-05-08 00:00:00-04 |   954 |  1
 B      | 2019-04-10 00:00:00-04 |   639 |  2
 B      | 2019-03-31 00:00:00-04 |   989 |  3
 C      | 2019-05-08 00:00:00-04 |   594 |  1
 C      | 2019-04-30 00:00:00-04 |    28 |  2
 C      | 2019-04-13 00:00:00-04 |    61 |  3
 D      | 2019-05-08 00:00:00-04 |   160 |  1
 D      | 2019-04-30 00:00:00-04 |   432 |  2
 D      | 2019-04-02 00:00:00-04 |   102 |  3
 E      | 2019-05-08 00:00:00-04 |    49 |  1
 E      | 2019-04-10 00:00:00-04 |   307 |  2
 E      | 2019-04-02 00:00:00-04 |   674 |  3
 F      | 2019-05-08 00:00:00-04 |   773 |  1
 F      | 2019-04-30 00:00:00-04 |   918 |  2
 F      | 2019-04-13 00:00:00-04 |   799 |  3
(18 rows)

```

The window definition in our `ROW_NUMBER` function has two critical parts: 

- `PARTITION BY` which defines the columns we want to group by
- `ORDER BY` which defines how the numbering will be applied to the windowed rows

Because we defined our window as "grouped by" metric and "ordered by" date descending, the most recent date for each metric will always have a value of `1` in the row number column.

With the numbering in place, we can run the numbering query as a subquery and pull out `rn = 1` for the final results:

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
    ROW_NUMBER() OVER(PARTITION BY metric ORDER BY date DESC) AS rn
  FROM
    metrics
) m
WHERE rn = 1;

```

Which leaves us with the full record for the most recent date of each metric:

```

 metric |          date          | value 
--------+------------------------+-------
 A      | 2019-04-30 00:00:00-04 |   889
 B      | 2019-05-08 00:00:00-04 |   954
 C      | 2019-05-08 00:00:00-04 |   594
 D      | 2019-05-08 00:00:00-04 |   160
 E      | 2019-05-08 00:00:00-04 |    49
 F      | 2019-05-08 00:00:00-04 |   773
(6 rows)

```