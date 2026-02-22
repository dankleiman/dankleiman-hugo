---
title: "Top N Per Group in BigQuery"
date: 2017-10-30 19:29:32 -0400
categories: 
- Code
- BigQuery
aliases: 
- "/blog/2017/10/30/top-n-per-group-in-bigquery/"
---
**EDIT:** After I posted this initially, I got some [great](https://twitter.com/Dan_Kleiman/status/925921880397287425) [feedback](https://www.reddit.com/r/bigquery/comments/7aecfe/top_n_per_group_in_bigquery/), so I wrote a follow-up post [here](/2017/11/07/more-efficient-solutions-to-the-top-n-per-group-problem/).

In this post, we are going to explore a strategy for collecting the **Top N results per Group** over a mixed dataset, all in a single query.

I stumbled onto this solution the other day, mostly driven by the fear that I was re-scanning my BigQuery data too often. At the time, the only way I knew how to look at a Top 10 list of a subset of the data was to add a `WHERE` clause limiting the whole data set to a single group and combine with `ORDER BY` and `LIMIT` clauses.

For each group, I would just modify the `WHERE` clause, rescan all the data, and get new results. I thought there had to be an easier way to get the same ordered subset for any particular group in the data, all at once.

It turns out, there is a much more efficient way to solve this problem.

<!--more-->

## Reddit Top 10 Users By Comment Score for July, 2015

Let's start with an example:

```
SELECT
  author,
  sum(score) as comment_score
FROM
  `fh-bigquery.reddit_comments.2015_07`
WHERE author NOT IN ('[deleted]', 'AutoModerator')  
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
```

I'm leaving out all query results in this post because it's a [public dataset](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_07?tab=preview) and you should totally go run the queries to see for yourself!

In the most straightforward way possible, we're summing up the comment score by author, ordering by highest score, and taking the first ten results.

While top commenters across all of reddit might be meaningful, you probably want to look at a specific subreddit.

```
SELECT
  author,
  SUM(score) AS comment_score
FROM
  `fh-bigquery.reddit_comments.2015_07`
WHERE
  author NOT IN ('[deleted]', 'AutoModerator')
  AND subreddit = 'webdev'
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT 10
```
By adding another filter to your `WHERE` clause you can now see relevant top commenters in a single subreddit.

This is what I was doing initially to inspect the dataset. I kept swapping out the subreddit in the `WHERE` clause and running the query again to view top commenters in different subreddits.

That was an okay first pass at understanding the data, but it's wasteful to re-scan the whole table every time to pull a single Top 10 result set. The better approach would be to get the Top 10 results for each subreddit all at once and store the results to its own table that you can then query for a single subreddit as much as you want. 

Also, if you ever wanted to build a data visualization tool off this view into the comment data, you wouldn't want to compute scores and rankings each time. So either way, working towards a single query makes a lot of sense.

## Top 10 per Subreddit

So far we have a pretty easy way to either get the Top 10 of the whole set or the Top 10 of a subset of the data. 

Now let's look at a technique for getting the Top 10 of each subset all at once. Thanks to this [stackoverflow post](https://stackoverflow.com/questions/44680464/get-top-n-records-for-each-group-of-grouped-results-with-bigquery-standard-sql?answertab=votes#tab-top), I had a solution, but I wanted to understand how to get to that solution from the "one Top 10 at a time" approach.

### ROW_NUMBER()

First, we need a way to order the commenters by score within each group. The key here is using the analytic function `ROW_NUMBER()`. [In databases, an analytic function is a function that computes aggregate values over a group of rows.](https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#analytic-functions)

```
SELECT
  subreddit,
  author,
  SUM(score) AS total_score,
  ROW_NUMBER() OVER (PARTITION BY subreddit ORDER BY SUM(score) DESC) AS comment_rank
FROM
  `fh-bigquery.reddit_comments.2015_07`
WHERE
  author NOT IN ('[deleted]',
    'AutoModerator')
GROUP BY
  1,
  2
ORDER BY
  1,4
```

This query will give us every author who commented in every subreddit with their aggregate comment score, _ranked by their comment score within the specific subreddit_.

We used the `ROW_NUMBER()` function to create an ordered list of scores, highest to lowest, by partitioning the data in a way that looks a lot like our second query, where we ranked comment scores from a single subreddit.

We're almost there!

We've got relative rank of each author within each subreddit in one query, but what we're missing is our Top 10 List for each subreddit. The query above still gives us all authors for all ranks.

### Subquery FTW

Unfortunately, we can't just put a `WHERE` clause like `comment_rank <= 10` into the query or use a `HAVING` constraint on the `GROUP BY`. Instead, we need to do a subquery to select from the ranked data:

```
SELECT
  subreddit,
  author,
  author_count,
  total_score,
  comment_rank
FROM (
  SELECT
    subreddit,
    author,
    SUM(score) AS total_score,
    ROW_NUMBER() OVER (PARTITION BY subreddit ORDER BY SUM(score) DESC) AS comment_rank,
    COUNT(DISTINCT author) OVER (PARTITION BY subreddit) AS author_count
  FROM
    `fh-bigquery.reddit_comments.2015_07`
  WHERE
    author NOT IN ('[deleted]','AutoModerator')
  GROUP BY
    1,2
    )
WHERE
  comment_rank <= 10
  AND author_count > 9
ORDER BY
  1,5
```

We are pulling all results where the `comment_rank <= 10`, meaning positions 1-10 in each subreddit by aggregate comment score. And just as a way of cleaning up the data even more, we added in the `author_count` column so that we can ensure that each subset has at least 10 authors -- we'll get a full Top 10 for each of the subreddits in our result.

### Verification

To verify this data, you can pick out any subreddit in the result set and compare it to the single subreddit query (the second query in this post) above. Spot any differences? We'll leave it as an exercise to the reader to figure out a tie-breaker strategy if we really wanted to ensure the same Top 10 results every time.