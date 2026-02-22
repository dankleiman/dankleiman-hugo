---
title: "Launching Datastroyer"
date: 2014-07-02 21:29:17 -0400

categories: 
- Code
- Launch Academy
aliases: 
-  "/blog/2014/07/02/launching-datastroyer/"
---

I'm very excited to announce that [Craig McGinley](https://github.com/craigmcginley) and I have launched [Datastroyer](http://datastroyer.herokuapp.com/).

Datastroyer is our online tool for searching JSON objects and returning the correct path to any value.
<!--more-->

Previously, I wrote about the [challenges of parsing compound data structures](/blog/2014/05/25/building-a-learning-tool-for-compound-data-structures/). For someone just learning to code and work with data, one of the biggest challenges was learning to read syntax.

One particularly challenging "reading problem" is figuring out how to reference a specific value nested inside a tangle of hashes and arrays. Not knowing how the object is structured, in terms of size, layers of nesting, or type of nested objects initially made this problem really confusing!

Eventually we learned how to traverse the whole structure and efficiently store the path we were going down as we went.

Craig and I have talked about many different use cases for the method we coded up, but in this case we have released the code embedded in a web application that searches JSON objects for you. If you've been working with API and trying to make sense of your queries, we hope this helps!

Here's what you do:

1. Copy your entire JSON object.

2. Visit [Datastroyer](http://datastroyer.herokuapp.com/).

3. Paste the JSON into the search box.

4. On the next screen, enter the search value you are looking for.

Datastroyer will return all of the possible paths to this search value inside of the JSON.

If you don't have some JSON to search, you can [try a sample search](http://datastroyer.herokuapp.com/data) with the data we've provided.

At the end of the day, we think this is a learning tool to help you get more familiar with the structure of compound objects.

We hope you learn like we have!
