---
title: "Burlington Ruby Conference 2014"
date: 2014-08-03 06:24:53 -0400
categories: 
- Code
- Ruby
aliases: 
-  "/blog/2014/08/03/burlington-ruby-conference-2014/"
---
It's 6:23 on Sunday morning, day 2 at [Burlington Ruby](http://burlingtonrubyconference.com/), so I thought I'd take a few minutes and recap some of what I saw and learned yesterday.

Everyone keeps talking about what an amazing community we have in the Ruby world and I guess I'm spoiled since I don't have any other software communities to compare it to, but I can tell you that every talk has been thoughtful, curious, and in different ways caring: caring about the future of the language, caring about other people's growth and development, and caring even about novel, smarter, and more refined approaches to getting things done.
<!-- more -->

In his keynote to kick off the conference, [Ernie Miller](http://erniemiller.org/) did a pretty amazing job capturing these core themes. I don't know how much people realized it, but he subtly set the tone for all the other talks too, both in terms of the human side of software development, but he also gave us context for all the non-Ruby or Ruby-divergent topics people were dying to discuss. Very impressive!

Here are a few of the ideas from the talks that jumped out at me.

How You Work with Other People
------------------------------

Having just come out of Launch Academy, I was really interested to hear what [Jennifer Eliuk](http://jennifereliuk.com/about/) had to say about apprenticeships.

While her talk definitely resonanted with me and helped me see "the next step" in my coding journey, she made a strong case for the importance of apprenticeships for the community at large.

Apprenticeships, for code school graduates or self-taught coders, have the potential to become a criticial rung on the software development ladder because:

- companies can groom and develop their junior talent, without all of the performance pressure of the day-to-day job.
- mentorship and teaching becomes a rewarding way for senior developers to grow in non-technical dimensions.
- a teaching culture also encourages learning -- she cited cases where she and senior devs would tackle new technologies side by side where everyone was learning together.

At Launch Academy, the staff and instructors were gradually and deliberately refining each piece of the learning process, not unlike the way they taught us to tackle complex software problems. Jennifer's talk was a perfect example of how to more broadly apply those same principles to the question: "how do we cultivate developers."

In fact, she argues, now that so much effort is being poured into the initial stage of learning, like code schools and weekend intro events or online curricula, we have to be more thoughtful about the next incremental step between kickoff and a dev career.

How You Write for Other People
------------------------------

Along the lines of incremental improvement and developing people, [Nicole Fenton](http://nicolefenton.com/) pushed everyone think hard about how their apps get users what they need.

Specifically, how do the "strings" or "micro-copy" or small cues and instructions that guide someone through a piece of software actually help them or are they just robotic, systems-focused, impersonal, confusing signposts.

One example she shared was from Square, when you send someone money. The confirmation email you receive basically says "You sent So-and-So $50." Simple, right?

Well, she had plenty of counter-examples that would have been equivalent to "We have received your request to transfer funds to user XXXX. We are accessing the database to store your request and .....typically processing time for this request...." Or something full of jargon and procedures that are necessary from the software's point of view but completely irrelevant to the goal the user is trying to accomplish.

So, the next time you write copy for a button, an error message, or a confirmation, ask yourself, "what was the user trying to do and where do they need/want to go next? Am I helping them along that path in a way they'll understand?"

How You Build for Other People
------------------------------

Both [Dan Luchi](http://danluchi.com/) and [Alan Peabody](http://alanpeabody.com/) grappled with what I'm coming to understand as the Rails identity crisis: *with an increase in mobile usage and connection speeds that enable heavier lifting client-side, what's a server-side web framework to do?*

The answer a lot of people are turning to, is that Rails is a powerful way to work with data and serve up an API that any front end view can consume.

I've even heard people advocating for further decoupling functionality within Rails apps, so that each service serves its own API to the others, which seems to have advantages for maintainability and deployment.

In these talks, though, the focus was mostly on getting a Rails backend to support and interact smoothly (and quickly) with whatever frontend -- mobile or web -- the user chooses.

Alan explained some of the challenges and solutions he's come up with for optimizing these connections and Dan gave us some great guidlines around functionality when deciding the best structure for building an app, like [Ticket Zen](http://www.ticketzen.com/), the parking ticket payment app I hope I never have to use.




