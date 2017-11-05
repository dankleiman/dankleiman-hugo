---
title: "Nice Try, NilClass"
date: 2016-04-10 07:13:27 -0400
categories: 
- Code
- Ruby
aliases: 
-  "/blog/2016/04/10/nice-try-nilclass/"
---

I love that feeling when a new concept starts to come together in your mind and you can point to all the converging sources of insight.

Right now, I can't tell if I'm fooling myself, hiding some logic, or making my code more readable with this particular concept, but when I put together these three pieces of information, I think I start to see something emerge.
<!-- more -->

I've been inspired to do some more digging into these kinds of questions lately thanks to the awesome new [Ruby Book Club Podcast](http://rubybookclub.com/). Co-hosts [Nadia Odunayo](http://twitter.com/nodunayo) and [Saron Yitbarek](http://twitter.com/saronyitbarek) are leading us chapter-by-chapter through different Ruby books and sharing their thoughts on the podcast as they go.

This week, specifically, I came across:

 - Damir Svrtan's article about [whitelisting input with #presence_in in Rails](https://infinum.co/the-capsized-eight/articles/whitelisting-with-the-lesser-known-presence-in-method).
 - [Avdi Grimm's Confident Ruby](http://www.confidentruby.com/) where #fetch is used to pull data out of hash.
 - A work situation, we were cleaning up #present? checks on incoming params input using #presence

I still don't know exactly what to call this collection of methods, but they all feel very related to me. They all remind me of [#try](http://apidock.com/rails/v4.2.1/Object/try), which makes me nervous.

Using #try always feels like a little bit of a crutch, where you don't quite know what inputs you are expecting or haven't coded thoroughly to all your cases, but in Rails, #try swallows some of the errors you would have run into and returns nil instead.

With these three methods, we're doing something similar. In each case, we get a simple way to check for a value and handle missing values gracefully with defaults, moving forward if the value is present.

So, for #presence, instead of:

```ruby

params[:name].blank? ? params[:name] : nil

```
We can do:


```ruby

params[:name].presence

```

 For whitelisting, instead of:


```ruby

if params[:name].present? && %w(foo bar).include?(params[:name])
  params[:name]
else
  nil
end

```

We can use #presence_in like this:

```ruby

params[:name].presence_in %w(foo bar)

```

Finally, with #fetch, the only Ruby standard library method in this group (the rest come from Rails), you have a few different options. Lifted straight from [the docs](http://ruby-doc.org/core-2.2.0/Hash.html#method-i-fetch):

```ruby

h = { "a" => 100, "b" => 200 }
h.fetch("a")                            #=> 100
h.fetch("z", "go fish")                 #=> "go fish"
h.fetch("z") { |el| "go fish, #{el}"}   #=> "go fish, z"

```

With #fetch, you use a key to puull a value from the hash, but you now you can define a default as your second argument, which is used to rescue missing key errors. Even better, you can execute whole block in the case that your key is not there.

Bonus Reading
-------------

I went digging a little more because I was still feeling uneasy about #try, but I couldn't quite articulate why. Guess who I found to say it for me? [Here's Avdi from 2011 on Structural Coupling enabled by #try](http://devblog.avdi.org/2011/07/05/demeter-its-not-just-a-good-idea-its-the-law/):

<blockquote>
<p>The seed of this all-too-common predicament is structural coupling. What’s structural coupling? To
define it, let’s start with a review of the DRY principle:</p>

<blockquote>"Every piece of knowledge must have a single, unambiguous, authoritative representation within the system."</blockquote>

<p>It’s easy to think about DRYness just in terms of data: e.g., there should be only one place in the
system for API keys; they shouldn’t just be copy-and-pasted willy-nilly throughout the codebase. But
DRY applies equally to structural knowledge: knowledge about the composition of and relationships
between your objects.</p>

<p>Let’s take a look at the code we started out with:</p>

```ruby
def user_info(user)
  "Name: #{user.name}. Dept: #{user.department.try(:name)}"
end

```

<p>This seemingly innocuous code makes the following assumptions:</p>

<ul>
  <li>user will have a name property.</li>
  <li>user may or may not have a single department.</li>
  <li>user's department, in turn, has a name property</li>
</ul>


<p>By going two levels deep into user's associations, we’ve made a structural coupling between this code and the models it works with. We’ve duplicated knowledge about a User’s associations—canonically located in the User and Department classes—in the #user_info method.</p>

<p>And the #try method was an enabler. By papering over the ugly user.department && user.department.name construct we’d otherwise have had to use, #try made the coupling an easier syntactical pill to swallow.</p>
</blockquote>

I highly recommend you read the whole article, as he goes into how this coupling violates the Law of Demeter and links back to [an earlier discussion of #try](http://devblog.avdi.org/2011/06/28/do-or-do-not-there-is-no-try/), because, clearly, while these types of methods are cool and convenient, they make him a little uneasy too.
