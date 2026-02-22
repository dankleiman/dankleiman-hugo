---
title: "Building a Learning Tool for Compound Data Structures"
date: 2014-05-25 09:07:15 -0400
categories: 
- Code
- Launch Academy
aliases: 
-  "/blog/2014/05/25/building-a-learning-tool-for-compound-data-structures/"
---

One of the most challenging things about learning to work with compound data structures has been reading the nested hashes and arrays and extracting the right set of brackets to use to identify a particular value in your code.
<!-- more -->

For example:
```ruby

    movie = {
      title: 'The Nutty Professor',
      cast: [
        {
          name: 'Eddie Murphy',
          characters: [
            'Sherman Klump',
            'Buddy Love',
            'Lance Perkins',
            'Papa Klump',
            'Mama Klump',
            'Grandma Klump',
            'Ernie Klump'
          ]
        },
        {
          name: 'Jada Pinkett Smith',
          characters: [
            'Carla Purty'
          ]
        }
      ]
    }

```

If I want to find a character, I have to reference an array inside a hash inside an array inside a hash...I think. Even that last sentence was difficult to write.

So I started thinking...there must be a programmatic way to express finding the reference for any element of the compound data structure.

Decompose the Problem
---------------------

Here's the problem statement:  **Given a value and a compound data structure, return the position of the value in the strucure, formatted so you can referrence it in your code.**

The first thing you realize is that searching through a hash and array will work slightly differently. On the advice of my instructors, I separated out these cases and got to work on the smallest case first.

Breaking it down into steps looked something like this:

1. Solve just the array case first.
2. Start with the smallest possible array.
3. Add layers of nesting and make sure it still works.
4. Then, modify the searching for hashes.
5. Combine.

Most of the work happened in step 3, where we run into the problem of tracking the correct path to our value through recursive calls to the search method.

Struggling through the recursion in this problem, I started to wonder if I had traded one problem, learning to read compound data structures, for another: *figuring out recursive searching!*

Working through Search Recursively
---------

Check out the suggested search for "recursion" when you Google it:

<a><img src="http://i.imgur.com/3rKK7mF.png" title="Hosted by imgur.com" /></a>

Ha! Yeah, I clicked on "Did you mean? recursion" a few times just to check.

Anyway, since we don't know how big the data structure is, we have to keep searching through unknown elements, that could be value, hashes, or arrays that need to be looked through in turn as well.

This is a job for recursion!


Looking at [tree traversal search problems](http://en.wikipedia.org/wiki/Inorder_traversal#Depth-first), I realized I needed to move through a tree structure and needed to track where I was on the tree…but couldn't figure out at first how to track the path.

The first pass at the problem returned an array of every endpoint of every possible path. Each element of the returned "path" array came back as true or false relative to the value we were searching for…but there were no breadcrumbs to know what the path was for the true version. *To solve the problem, we needed to return a path, not just know that the value was in the data structure*

To identify the path, we capturing the index of the current element we were testing in the array. We'd add them once we new we had a true path on the way "back up" the recursion. This was messing with the order, though.

Finally, (in the shower, of course!) I realized that adding to the path should happen just before the recursive call AND if the call came back "false", we should strip out the path identifier right after the call came back.

Adding to the path:
```ruby
    if !path.include?(true)
      path << i
    end
```
Removing the "wrong branch" from the path after the recursive call:
```ruby
    path = path_finder(value, element, path)
    if !path.include?(true)
      path.pop
    end
```

In other words, a "not-true" return would tell us that we went down the wrong branch and so we should erase that branch and start going down the next possible branch.

After I got the correct path to return, it was just a matter of cleaning it up and presenting it in a way that would let you "copy and paste" into your code for easy referrence.

I hope this comes in handy when other people are learning to read compound data structures!

[Check out the repo on Github](https://github.com/dankleiman/path_finder).

