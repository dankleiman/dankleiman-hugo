---
title: "Don't Blow Your BigQuery Budget on Unknown Data!"
date: 2017-10-06 14:55:37 -0400
categories: 
- Code
- BigQuery
aliases: 
-  "/blog/2017/10/06/dont-blow-your-bigquery-budget-on-unknown-data/"
---
It's easy to blow your BigQuery budget when you are exploring a new data set. Because you're billed for the amount of data scanned, not the ultimate result set, when you don't know what you're looking  for, you can end up with wasteful queries.

In this post, I'm going to share some tips for more efficiently scanning data in BigQuery when you don't quite know what you need.
<!--more-->

To ground some of these questions in an example, at work, we often investigate unknowns in our data, especially where we integrate with third parties. Recently, we were reconciling some data with a third party that posts us back about in-app events. They had about 50,000 events for one month, and our logs showed that we processed 10,000. What happened to the delta? Who had the more accurate number?

The table in BigQuery that holds these particular event logs for us gets about 1 billion postbacks a day and the period in question was a whole month. So, without blowing my whole BigQuery budget, I had to poke at this large data set and explain how those 50k needles moved through our haystack of 30 billion requests.

If you're new to BigQuery, and drawing on your past experience with other databases, it's tempting to want to `SELECT * FROM whole_month_of_data`, export it to Excel, and do a `VLOOKUP` to see if their data is there...but as you're about to learn, that is the 100% wrong approach to efficiently working with data in BigQuery.

Now, I can't share our actual queries and data with you for this particular case, but fortunately, [Google makes public datasets available](https://cloud.google.com/bigquery/public-data/) to anyone using BigQuery. And you can start to play around on their free tier, provided you follow these tips to stay under the free allocation.

I used all these same techiniques to ultimately piece together a clear explanation of how the event data moved through our applications...and I only blew my daily BigQuery budget on the first day of this investigation.

## Never Use Select *

So, the first thing you should do when you open up a new dataset, is NEVER USE `SELECT *`.

If you're used to working with smaller row-based relationational datastores, like MySQL or Postgres, then `SELECT *` is a handy way to get a feel for what's stored in your tables.

However, in a column-based store like BigQuery, `SELECT *` is much less efficient. Instead, you want to explore column-by-column.

Here's a good explanation of the difference [between row-based and column-based datastores](http://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html). Basically, in a row store, the data for each row is stored continguously in memory on disk, so when you `SELECT *` and pull out the whole row, you're reaching for adjacent memory that is more easily pulled all at once. 

In a column-based store, the allocation is inverted, so the whole column of data is stored together, not the row. Every time you have to pull a new column to build your row, you're reaching somewhere else on disk, which is less efficient.

Pulling an entire column is going to be cheaper than pulling all columns, even if you do something like `SELECT * FROM whatever LIMIT 1` because each of the non-contiguous columns has to be scanned to get the data you need.

## Handy Preview Mode

If you need to explore an unknown data set, you can still get a feel for what's in each column and the different characteristics of the data by using BigQuery's built in "preview" function.

<img src="/images/bigquery_preview_mode.png">

I'm using [this publicly available dump of Reddit comments](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_01?tab=preview) for all the screenshots in this post.

Use preview to refine the questions you need to answer with the data and understand what data is available. When you find a potentially useful column, just query this column, grouping values or filtering results to understand what's there more thoroughly.

But remember, even here, you don't want to be crawling the whole data set you're ultimately interested in each time. Instead, try to limit it to a single shard of data -- in my work example above, that would have been a single day of data, even though I was ultimately going to have to scan a whole month.

## Run Your Big Query Once

Once you've identified the columns and clauses you need, run the "big query" once and store it to a temp table.

<img src="/images/bigquery_temp_table.png">

Now, instead of querying against billions of rows each time, you will be working with a subset of data. Even if it's a few million rows, it will still be more efficient.

## Import External Data

If you're comparing BigQuery data to external data, you might be tempted to export your BigQuery data at this point and try to compare data in spreadsheets. Don't!

Instead, you can import data into BigQuery as a temp table and use the auto-detect schema feature. BigQuery will build you a temp table with all the columns and rows from your spreadsheet.

<img src="/images/bigquery_import_data.png">

Now you can use your temp table or any other data set to write SQL against your external data. You can even join data across BigQuery projects -- the project name is just part of the namespace that identifies each table.

## Now Go Query

I know when I started working with data in BigQuery, I was always afraid I was going to scan too much data, or write bad SQL. I probably still do that on a regular basis, but hopefully, by following these guidelines, I've become a little smarter about how I tackle an unknown data problem.

And I hope you found at least one good tip in this post to go and use too!