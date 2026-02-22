---
title: "Asking Questions: The Holy Grail of OOP"
date: 2014-06-08 20:32:17 -0400
categories: 
- Code
- Launch Academy
aliases: 
-  "/blog/2014/06/08/asking-questions-the-holy-grail-of-oop/"
---

This week at Launch Academy, we started working on Object Oriented Programming (OOP).

We've been guided by the conceptual model that objects, which can have state and defined behavoirs, respond to methods the same way that you would respond to a question.

Of course, a week of asking my objects questions made me think of this:

<!-- more -->

<iframe width="640" height="480" src="//www.youtube.com/embed/pWS8Mg-JWSg" frameborder="0" allowfullscreen></iframe>

And the more I thought about The Bridge of Death, the more the Bridgekeeper's questions made a lot of sense in our OOP world.

Really, we've got a collection of Knights and each one responds to a series of questions. If we coded that up, it would look something like this:

```ruby
class Knight
  attr_reader :name, :quest, :favorite_color

  def intialize(name, quest, favorite_color="blue")
    @name = name
    @quest = quest
    @favorite_color = favorite_color
  end

end
```

Our knights, Sir Lancelot, King Arthur, or Sir Galahad, are all instances of the class "Knight." They are objects with contain a state (their specific names, quests, etc) and behaviors.

When it comes to behaviors, they can inherit them in some cases, or the behaviors have to be explicitly defined within the class.

In the clip above, we can see how the knights know how to answer the questions about their names and quests...they respond to the name and quest methods defined in their class.

But we also see something else.

When Robin approaches the bride, the Bridgekeeper asks him his name and quest:

```ruby
robin.name
robin.quest
```
And that produces the answers we'd expect:
```ruby
"Robin of Camelot"
"To seek the Holy Grail"
```
But then the Bridgekeeper throws a curveball. He calls
```ruby
robin.capital_of_assyria.
```
When Robin is asked what the capital of Assyria is, he literally blows up. From an OOP perspective, we know it was because this behavior was never defined for the class Knight:

```ruby
def capital_of_assyria
  ????
end
```

Of course, there's a further twist when the Bridgekeeper tries to call
```ruby
.airspeed_velocity_of_an_unladen_swallow
```
on King Arthur, but really, you should watch the clip if you don't already know what happens.

Asking Questions, Building Objects
----------------------------------

So, now we know that you have to define the behaviors you want to utilize to do effective object-oriented programming.

But why? What's the point? Or more importantly, what's the advantage of writing code this way.

I'm sure there are bigger implications of taking this approach, but I can tell you that right away, my experience of writing simple code is completely different.

When you set out to build classes and objects, you actually don't need to know everything about how your program works right away to make progress.

Instead of figuring out every detail of every loop, calculation, and variable, **you can assume that the classes and methods you create will give you the answer you want.**

You are free to write more semantic, flowing code from the beginning, without having to stop and figure out the nitty-gritty.

Even in my limited experience taking this approach, I can tell you that it lets you think at a high level about your problem, sketching out the logic, flow, and just marking out the big areas you know you'll tackle later on.

Gradually, layer-by-layer, you go deeper and work out the details.

I wish I had had a clear top-down model like this to solve problems in the past. Here's to applying it going forward!

