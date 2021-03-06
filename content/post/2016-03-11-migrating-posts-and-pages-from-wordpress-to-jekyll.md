---
layout: post
title: "Migrating Posts and Pages from Wordpress to Jekyll"
date: 2016-03-11 13:55:15 -0500
categories: 
- Code
- Static Sites
aliases: 
-  "/blog/2016/03/11/migrating-posts-and-pages-from-wordpress-to-jekyll/"
---

<em>This is Part 1 in a series on [Migrating from Wordpress to Jekyll](/blog/2016/03/09/migrating-from-wordpress-to-jekyll/).</em>

The documentation for [getting started with Jekyll](https://jekyllrb.com/docs/quickstart/) is great. I'm not going to rehash everything that's covered there.

Instead, this post and the others in the series will be more like, "here's the order I wish I had done things in" or "here's everything I ended up needing to pull together to get stuff working". I hope it helps you and saves you time if you ever decide to do a similar migration from a self-hosted Wordpress install to Jekyll.

So here we go....

<!--more-->

Migrating Posts and Pages
-------------------------

To migrate your existing posts and pages from Wordpress, here's what you need to do:

1. **Install Jekyll** and create a new instance in the directory of your choice (follow the commands [here](https://jekyllrb.com/docs/quickstart/) -- you can even run `jekyll serve` to see the boilerplate of the site you just created).
2. **Export a copy of your Wordpress database** (I was on WPEngine and they have a good explanation of [how to export from phpMyAdmin](https://wpengine.com/support/exporting-database/)).
3. If you don't have it already, **you will need mysql installed** to work with the Wordpress database -- using homebrew you can `brew install mysql`.
4. **Create a new database** through your mysql console and use the source command to load the .sql file you exported in step 2: that's `mysql -u root` to acces the console, then `CREATE DATABSE whatever_you_want_to_call_your_wordpress_db` to create a new database, `use whatever_you_want_to_call_your_wordpress_db` to start using the database, and finally, `source the_file_you_exported.sql` to load all the data.
5. Now we're ready to use the **Jekyll Importer for Wordpress**. You'll need a few more gems installed to be able to read from mysql ([see importer docs](http://import.jekyllrb.com/docs/wordpress/)), but then, with a local copy of your Wordpress database, the import will be pretty straightforward.
6. **Inspect your new Jekyll posts and pages**: the import will dump all your Wordpress posts into a directory called '\_posts'. I don't know what this will look like if your Wordpress permalink structure does not have the YYYY-MM-DD-post-title format, but Jekyll relies on this date format when generating your site. In other words, an html file like this: '/_posts/2016-03-11-migrating-wordpress-posts-and-pages.html' will be turned into a page at http://your-domain.com/some-category/2016/03/11/migrating-wordpress-posts-and-pages.html. You can ultimately tweak the permalinks, but the actually page generation seems to rely on the date format in the source post file name.

A Note about Pages
------------------

If you had a lot of pages in Wordpress, you will find that the import has created directories named after these pages in the root directory of your Jekyll install. Inside each of these directories is an index.html (or whatever you specified in the importer, i.e. md) file with the actual html content from your Wordpress site.

I haven't completely decided what to do with these pages for my site yet. In some cases, they are no longer relevant because they reference features of the site I won't be supporting in this "archive" version of the old site.

In other cases, though, they contain content that could have easily been a post. For these post-worthy pages, I am moving them to the '\_posts' directory, changing the file name of the index.html file to use the date specificied in the YAML front matter generated by the importer (probably the published date of the page) and the name of the directory, so: index.html inside of '/some-great-page' that was published on 2014-05-31 becomes '/_posts/2014-05-31-some-great-page.html'. I like this approach because now when you build your site, Jekyll will automatically add this page to the list of posts in the correct chronological order.

Either way, I plan to minimalize the number of 'page' directories in the root of the site and use the conventions built up around posts in Jekyll to deliver as much of the content as possible (see below on categories and tags, for example).

Categories and Tags
-------------------

Jekyll has some handy [global variables](https://jekyllrb.com/docs/variables/) built in that allow you to group posts together and display them and generally reference attributes about your site and its contents.

Specifically, as I was thinking about how to structure the new site, I was wondering about different ways to group posts together, based on the categories I had used in the Wordpress site, instead of just displaying one long reverse-chronological list.

I found [this excellent post on extending some basic layouts to take advantage of categories](https://codinfox.github.io/dev/2015/03/06/use-tags-and-categories-in-your-jekyll-based-github-pages/). Incidentally, hosting on Github Pages, which I plan to do, limits the number of Jekyll plugins you can use, but that's fine with me.

Taking the approach from the article above, if you want to show all Tai Chi posts on one page, you create a page called 'Tai Chi Articles' and set its category as 'Tai Chi'. You specify the layout as 'category', which you build in your '\_layouts' directory.

In the new layout, you are iterating through all the posts and checking for a match to the category specified on the page that uses that layout.

In other words, on the 'Tai Chi Articles' page, you are iterating through all posts that have the category 'Tai Chi' and linking to them in this list. And I keep having to remind myself, this happens during the build, so you generate a nice, quick-loading page!

With my categories set up and pages repurposed as posts or eliminated, I felt like I was making good progress on the migration.

Of course, questions about redirection from the pages I converted or deleted and styling and layout started to fill my head...but we're going to get to that in future articles!
