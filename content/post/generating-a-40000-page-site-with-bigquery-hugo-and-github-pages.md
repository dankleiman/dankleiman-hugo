+++
date = "2017-11-18T14:38:49-05:00"
title = "Generating a 40,000 Page Site with BigQuery, Hugo and Github Pages"
featured = ""
linktitle = ""
description = ""
categories = ['Code', 'BigQuery', 'Hugo', 'github-pages']
featuredalt = ""
featuredpath = ""
author = ""
draft = true

+++

Recently, I've been poking at Reddit datasets on [BigQuery](/categories/bigquery) and consolidating the [code](/categories/code) and [Tai Chi](/categories/tai-chi) sections of this site onto a single Hugo site, hosted on Github Pages.

So I thought, why not come up with a small project that combines them? Well, 40,000 pages later, I sure came up with something.

<img src="/img/too_many_files.png" alt="Too many files makes Github sad">

Oops!

We'll look at when went wrong or wasn't exactly convenient about this approach, but first, let's talk about the what the project is and its three main pieces.

## Crosslinking Subreddits on Reddit

I had been exploring [this Reddit comment data](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2017_10?tab=preview), which includes the actual comment body and which subreddit it was posted in. After a while scrolling through comments, I started thinking about 