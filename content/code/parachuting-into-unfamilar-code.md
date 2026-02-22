---
title: "Parachuting into Unfamilar Code"
date: 2015-01-11 20:15:27 -0500
categories: 
- Code
aliases: 
-  "/blog/2015/01/11/parachuting-into-unfamilar-code/"
---
We have hundreds of models in our codebase at [TrialNetworks](http://www.trialnetworks.com).

As a new developer, the first 12 features I was asked to work on didn’t touch the same parts of the code. In terms of learning our product, I think that was good, but without some serious “orienteering” practice, it was also confusing and frustrating.

I felt like I was being pushed out of a plane in the middle of the night, with a backpack full of gear, a tiny map, and some night vision goggles, and I was told to rendezvous in 6 hours in a place I’d never heard of before.

In fact, I still get this feeling, every time I’m asked to work on a new module in our platform.

So when you jump out of the plane, how do you land, get your bearings, and complete the mission?

<!--more-->

I’m sure there are other ways to do it, but here’s my current strategy.

Start at the End
----------------

The paratrooper analogy is about to break down on us, but when I’m working on a feature, even if I somewhat understand what the problem is at the database level, or what new controller actions we will most likely create, I’ve found it easiest to get my bearings by **starting with the view** – or the interaction that the user will have.

When you start with the view, you can:

- See how the software is currently functioning
- Note what additional screens, tabs, links, buttons, or data need to be rendered
- Break open the code and look at how the current interface is being generated

Once you get to the last step, and you’re in the code, exploring how we are rendering something, you start to work up strategies for tackling the problem.

In an existing codebase, other people have left clues. You see assumptions about how they arrived at generating the current behavior and your next steps are revealed.

Tracing Someone Else’s Path
---------------------------

**Start tracing the path backwards from the url.** In Rails, there are strong conventions about which controllers and which actions are generating the view you are looking at.

Armed with the url, you know which controller is routing data to the view you are working on. As you start to see which models are being used in the view, you can further construct the path.

At this point, I like to change analogies again.

Who (which models) showed up to the party (the view), and who’s throwing the party (which controller/action)?

I build a sort of working guest list for the party and start to think about **who I want to talk to and who I will ignore.**  Narrowing in on the behavior you are going to modify or figuring out where you want to insert new behavior is like working the room until you find the right place to hang out.

What You Bring to the Party
---------------------------

At this point I really don’t know what analogy to go with, but once I’ve found my spot in the room, I can relax a little.

See, I know I’ve ruled out 98% of the codebase in terms of things I will have to touch to get this feature done.

Back when we were jumping out of the plane, I was worried. I didn’t know the terrain at all. Before I looked at the view, it could have been any of the tens of thousands of lines of code that needed to be touched to make it work.

Now, I know where I am. I’m in the right room, in the right mansion, at the right party…*do the analogies hold together better if I had jumped out of the plane in a tuxedo, like some James Bond-esque super spy???*

In any case, now the focus is incredibly narrow. Most of the time, we’re not only in the right controller, but it becomes clear that a specific controller action needs to be tweaked, or a new one needs to be added.

From here, I like to **pseudo-code the behaviors I want.** Pseudo-coding, as I learned it, was more or less writing a series of comments that kind of look like code, but act more like a step-by-step guide for what you want to accomplish.

The benefits of pseudo-coding are:

- I can write it a lot faster than I can if I’m stopping to check if every line is working
- I can have a “complete thought” in the pseudo-code without stopping to dig around and see if a similar method has been implemented somewhere else
- **Bonus:** completing the thought also acts like a sounding board. It either confirms that I am in the right place, taking the right approach, or gives me new insight into how to create the feature

From pseudo-code, you can work out the nuts and bolts of implementing the feature, but the task is pretty well, i.e. narrowly, defined at that point and you usually only end up writing a few lines of code.

In fact, I think I’m starting to see that if in the end you aren’t writing small amounts of code in a narrowly defined scope, you haven’t worked the room enough to find the right spot…but I have a feeling I’ll be arguing for or against that assertion more in future posts.

Hoofing it back to the Rendezvous Point
----

We got in, completely our mission, and got out. The final (haha!) stage of the process is the extraction moment. As you’re being plucked off the ground and back into the sky, you get a final bird’s-eye view of the code.

Either this is a moment of satisfaction, as you survey your work, or someone comes along and pushes you out of the plane again, to redo the whole mission.
