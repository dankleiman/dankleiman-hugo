---
title: "Buying a Mongolian Website for my URL Shortner"
date: 2014-05-30 09:17:22 -0400
categories: 
- Code
- Launch Academy
aliases: 
-  "/blog/2014/05/30/buying-a-mongolian-website/"
---

Ok, so technically I just purchased a Mongolian domain name: [klei.mn](http://klei.mn).

Why, you might be wondering?
<!-- more -->
This week at Launch Academy we've been building Sinatra applications with simple databases (Redis and Postgres) and deploying them to Heroku.

One of the extra-credit projects was to build a url shortner and I thought it would be cool to hook mine up to a customized domain, kind of like a vanity plate for your car.

In this post, I'm going to explain why you might want a URL shortner and how I built and deployed my own custom version.

The Basic Logic of a URL Shortner
---------------------------------

Sometimes, when you're sharing the url of a website, the address can be really, really long.

This is problematic if you're trying to dictate the url to someone, have to write it out by hand for some reason, or if you want to share it somewhere with space constraints, like on Twitter.

The idea behind a url shortner is that you can generate a shorter url whose sole purpose is to redirect to the longer url. Now, you can use a much shorter, more manageable set of characters to describe the same page.

Often, the domain of the url itself is only a few characters long, further truncating the "short url" -- examples include Twitters own service, t.co, or a free service anyone can access like bit.ly.

Many sites like the New York Times have created prorietary domains just to shorten their own links, which is a combination of branding when the short domain resembles the name of the company or main site and a tracking tool, which I'll explain more further down this post.

My Mongolian Domain Name
------------------------

So, when I said this was a bit of a vanity project for me, what I meant was, I took my last name "Kleiman" and tried to think of a way to shrink it down to fit a small domain name.

Using something like "DansShortUrlforShorteningLongUrls.com" would totally defeat the purpose, right?

I had seen the ".mn" Top Level Domain (TLD - that's the extension on any url, like .com), so I poked around a little to see about purchasing one.

It turns out that the more obscure TLDs aren't for sale on all of the popular domain resellers, but after a little digging, I did [find a site](http://domain.mn) that sells .mn domains -- and it turns out that the country that owns that TLD is Mongolia.

Nothing like starting your morning off with a little international commerce!

The Final Step: Deploying the App
---------------------------------

So, last thing first, then we'll talk about the code.

When you deploy an application to [Heroku](http://heroku.com), they host your code on a server and set you up with a subdomain.

Their subdomains are pretty elegantly named. They always conjure dark, quiet, rustic imagery, like "sleepy-journey" or "damp-retreat".

Again, though, the problem is that "stormy-stream-3295.herokuapp.com" doesn't really lend itself to a short url.

I saved this for the final step, but after the app (ok, version 1) was up and running, I went through the process of redirecting the Heroku default domain to my newly acquired, shorter Mongolian domain name, klei.mn.

Just want to give a shoutout here to [DNSimple](http://dnsimple.com) for making the redirect process really painless. Initially, I tried to mess around with the records that tell any requests from the browser where to go for the page you want on the site where I bought the domain name. It was a mess.

Fortunately, DNSimple has an easy process for redirecting and within minutes, the app was running from Heroku on klei.mn. Really Simple!

The only other hiccup I encountered in deployment was that the free Redis database I was using kept timing out with the number of requests the app was making, even for some simple testing. Since we had moved on to Postgres in class, I rewrote the app to use that instead. As it turns out, the data structure in Postgres was much easier to use anyway, even if it was probably overkill, with a single table in this case.

I hope to come back to the differences in working with these two databases, but that's for another time and post.

Building the URL Shortner in Sinatra
------------------------------------

At Launch Academy, we've been following a really neat learning progression, where we're building up gradually to the complexity of a full stack web application, specifially built with Ruby on Rails.

While we've been working on our Ruby fundamentals all along, there are at least three other areas that can be broken down into simpler steps:

+ The Framework that integrates what the user sees with the information stored in the database.
+ The Database, in terms of its organization and how the application interacts with data.
+ The Front-End interaction for the user.

For this project, I'm going to explain where we're at mainly regarding the framework.

We started out with the simplest way to run a Ruby program, executing a Ruby file from the command line.

When we were just learning Ruby, this was fine. We didn't have a lots of data and the programs were simple enough that all of the logic could easily fit in one file. Plus, the interface was bare bones, just the simple, elegant command line (I'll probably write more about falling in love the command line later, ha!).

And even when we wanted to use more complex data, we learned how to read and write with local files or even pull in data from APIs.

To persist information and access it more dynamically, though, we quickly ran up against the limits of our CSV files and started to need to query databases.

Interacting with a database leads to moving dynamic information around between all your different files, selectively displaying it to you user.

To control the data this way, you need an extra layer, between the user and the database, essentially to direct all this traffic and figure out what to do next. Enter, "the framework." In this case, we started out with a simple one (I'm told) called Sinatra.

In production, your Sinatra app likely includes the following files:

+ A file to tell the server how to being your program.
+ A "server" file that the program runs from, directing traffic, executing program logic, and interacting with the database.
+ "Views" that dictate what gets displayed on each page the application serves up.
+ In Ruby, "Gemfiles" that tell the server what Ruby Gems will be needed to perform specific tasks in the application.

From what I understand, compared to a more robust framework like Rails, Sinatra's simplicity lies in the way all of your routes (links between the data and the views) live in a single file.

At least for us, at this stage, it made sorting out all the program logic easier, since you only have to look in one place. One the flip side, I can see how this gets messy as you go up in complexity, but that's what's cool about our curriculum: when increased complexity/difficult necessitates new tools to handle the issue, we are introduced to them, *but not before*.

And Now for Some Code
---------------------

There are two operations at the heart of this project: **creating short urls and redirection**.

I want to turn the long url that you give me into a short one AND every time you visit the short one, I want to send you to the long one.

Along the way, if I can [track how often this is happening for each short url](http://klei.mn/stats), that will be cool too.

When you visit [klei.mn](http://klei.mn), hopefully, the action is clear: give me a url to shorten.

Here's what the shortening code looks like:

```ruby
post '/new' do
  url = params[:url]
  @errors = []
  @errors = valid_url(url)
  if @errors.empty?
    long_url = check_long_url(url).to_a
    if long_url.empty?
      short_url = get_short(url)
      save_link(url, short_url)
    else
      short_url = long_url[0]["short_url"]
    end
    redirect "/links/#{short_url}"
  else
    erb :index
  end
end

```

Here's what it does:

+ Once you hit "Shorten" on the main page, you send the server the "post" request.
+ First, I'm going to make sure what you put in the form is a valid url.
+ Then, I want to check and make sure that the url you sent me isn't already in the database.
+ If it is, I will send you to the page that already exists for that link: klei.mn/links/(some short url), that shows the full url, the short url, and click stats.
+ If it's not in the database, I create a new short url for it and insert that new info into the database with the "save_link" method.

Check out the stats page for [all shortened urls](http://klei.mn).

You'll notice that [one clever person](https://twitter.com/heroiceric) I asked to test the site started by shortnening the main domain, then kept entering the returned short urls into the shortner. Now, every time you use the last link, it redirects you to the main page, *via all the other shortened urls and all their click stats go up*. (I'll likely disable the ability to submit urls with klei.mn as the domain by the time you read this.)

Now that you've created or retreived a short url for your long link, you'll want to use it.

Here's what happens when you enter one of the short urls:

```ruby
get '/:short_url' do
  short_url = params[:short_url]
  if short_url == 'stats'
    @url_stats = get_all_url_stats
    erb :'stats'
  elsif short_url == 'about'
    erb :'about'
  else
    add_clicks(short_url)
    outgoing_link_data = get_long_url(short_url)
    outgoing_link = outgoing_link_data[0]["long_url"]
    redirect "#{outgoing_link}"
  end
end

```

Here's what's going on in the code:

+ First, I grab the slug, or the part of the url after "klei.mn/", from the "get" request.
+ Since all the short urls are klei.mn/something, there have to be a few exceptions for any other page I want to have on the site, like "klei.mn/stats" or "klei.mn/about". *Maybe there's another way to do this?*
+ Once I've determined that it's one of the short urls, I want to send you to the url you're actually looking for. But first, I want to increase the click count for that url. The first method, "add_clicks", adds a click to the counter for that url. Yay, semantic naming conventions!
+ Next, we need to go get the corresponding long url from the database, so we know where to send you.
+ Finally, we redirect to the long url.

Before I really knew how servers sent and received information, this whole redirecttion process seemed like a little bit of magic.

Writing this up, now, though, it all feels pretty straightforward, don't you think?

You ask me to go somewhere. I look up directions and send you on your way to the destination you actually want. Maybe this is a version of "give them what they want in the hope that they'll want what they need?"

Which leads me to a more dilemma about shortening urls....is it really what we want to be doing?

The Problem with URL Shortnening
--------------------------------

I mentioned this project to a former board member of the [Web Foundation](http://webfoundation.org, whose mission is to "establish the open Web as a global public good and a basic right, ensuring that everyone can access and use it freely." and he said "you know that's not a good idea, right?"

It's not that he's against me learning to code. He's been very supportive. ;-)

But what he and his colleagues do is think about the world wide web on a much longer time scale that most people typically do.

Our use case for the short url is really about convenience. They think about persistence, connectivity, and meaning.

By inserting short urls all over the place to direct connections around the web, we are potentially creating a lot of dead-ends if the short url domains go away.

From what I gathered from him, there is also a semantic isssue, when you compare short urls and their longer parents.

The short links posted everywhere won't really mean anything, compared to the more detailed long urls they are derived from.

Wikipedia has more on the shortcomings of URL shortnening [here](http://en.wikipedia.org/wiki/URL_shortening#Shortcomings).

Can you make the case either way? Does it make sense in a more closed ecosystem like Twitter? Am I being an irresponsible citizen of the net by introducing short urls for vanity and convenience?

These all seem like interesting questions!
