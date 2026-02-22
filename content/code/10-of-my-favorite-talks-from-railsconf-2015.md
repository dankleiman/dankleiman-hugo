---
title: "10 of My Favorite Talks from RailsConf 2015"
date: 2015-04-29 20:47:31 -0400
categories: 
- Code
- RailsConf
aliases: 
-  "/blog/2015/04/29/10-of-my-favorite-talks-from-railsconf-2015/"
---

RailsConf 2015 was a blast. There were talks on a such a wide range of topics, that I wanted to capture some of my favorites here.

Here's my Top 10 Countdown from the conference:

<!--more-->

I'll try to update as many of these as possible with video if/when they become available. For now, I've tried to gather as many slide decks as possible.

<ol reversed>
  <li>
    <strong>Designing a Great Ruby API - How We're Simplifying Rails 5</strong>
    <p>At times this one was over my head technically, but it was awesome to see a core contributor breaking down the process of how the inner workings of Rails are built.</p>
    <p>Sean is a presenter and was hanging out between talks fielding questions too.</p>
    <script async class="speakerdeck-embed" data-id="2a56dba370414cd1a48d1aa43d8fffab" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>
  </li>
  <li>
    <strong>Playing Games in the Clouds</strong>
    <p><a href="https://twitter.com/nodunayo">Nadia Odunayo</a> gets my award for Best Explanation by Analogy. Her talk captured at a high level how concepts from Game Theory concepts can be applied to allocating resources in distributed systems</p>
    <p>Very cool!</p>
    <script async class="speakerdeck-embed" data-id="46080b095191416dbc21ba9e9ec8084e" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
  </li>
  <li>
     <strong>What's Happening in Your Rails App?</strong>
     <p>Introduction to Introspection Features of Ruby</p>
     <p>Koichi Sasada is a member of the Ruby core team and works on "Matz's Team" at Heroku. He said, "I'm not actually a Rails developer, but my wife is, so she's my customer."</p>
     <p>This was another talk where the inner workings of technology we use every day are exposed...by the people actively maintaining them. I think that's so cool to see.</p>
     <p>Also, check out his definition of Event Driven Development.</p>
     <iframe width="815" height="458" src="https://www.youtube.com/embed/4YtBS0tvkjw" frameborder="0" allowfullscreen></iframe>
  </li>
  <li>
    <strong>The World of Rails Security</strong>
    <p>When <a href="https://twitter.com/presidentbeef">Justin Collins</a> broke down Rails security into "What Rails Provides," "What Rails Doesn't Provide," and "What to Do About It." Security seems like a Rubik's cube issue. You can look at it, and try to break it, from so many different angles.</p>
    <script async class="speakerdeck-embed" data-id="05e09bab40404a61a4d6b844109d84f3" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
  </li>
  <li>
    <strong>Processes and Threads - Resque vs. Sidekiq</strong>
    <p><a href="http://jdabbs.com/">James Dabbs</a> gave an awesome live demo of the internals of Resque vs. Sidekiq. Not only was it a pleasure to watch him fly through the code and take us right in to key points that differentiate these two job enqueing tools, but if you head over to his Gitub, you can actually run the same tests that he demoed in the talk:</p>
    <p><a href="https://github.com/jamesdabbs/railsconf-2015">Code</a></p>
    <p><a href="https://github.com/jamesdabbs/railsconf-2015/blob/master/slides.md">Slides</a></p>
  </li>
  <li>
    <strong>Why Your New API Product Will Fail</strong>
    <p>Despite evidence to the contrary, this talk was not about writing your API at the last minute:</p>
    <blockquote class="twitter-tweet" lang="en"><p lang="en" dir="ltr">Probably about time I wrote this talk...</p>&mdash; Scott Feinberg (@scottefein) <a href="https://twitter.com/scottefein/status/590878954568974336">April 22, 2015</a></blockquote>
  <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
    <p>Update: Here are Scott's slides:</p>
    <script async class="speakerdeck-embed" data-id="045b214b36734c1f8d2bd90396059073" data-ratio="1.29456384323641" src="//speakerdeck.com/assets/embed.js"></script>
    <p>The big takeaway from Scott's talk was very simple: your API is an interface that other developers will use AND so is <strong>your API documentation</strong>. When these suck, user experience, and user happiness, really suffers too.</p>

    <p>Scott dove into a lot of the tooling he's used to automate API documentation, but to think the job is just about tooling is another pitfall. You should care about every place people interact with your application. Even his automated solutions, he said, began with a lot of manual trial and error.</p>
  </li>
  <li>
    <strong>Keynote by Aaron Patterson</strong>
    <p>From a man who really doesn't need an introduction to be worth watching:</p>
    <iframe width="815" height="458" src="https://www.youtube.com/embed/B3gYklsN9uc" frameborder="0" allowfullscreen></iframe>
    <p>I just want to know if that part in the middle was staged or not.</p>
  </li>
  <li>
    <strong>Keynote by DHH</strong>
    <p><em>This video is almost 9 hours long, capturing the whole first day of the conference in the main room. Jump to about 24 minutes to catch the beginning of DHH's Keynote</em></p>
    <p>What I found most inspiring about this talk was the attitude that Rails can provide leverage. As a framework, a set of tools, individuals and small groups can write applications at web scale that do amazing things.</p>
    <iframe width="815" height="458" src="https://www.youtube.com/embed/oMlX9i9Icno" frameborder="0" allowfullscreen></iframe>
  </li>
  <li>
    <strong>Voila, Indexes!</strong>
    <p>A Look at Some Simple Preventative Magick</p>
    <p>This talk is a real treat. Not only does <a href="https://twitter.com/jamis">Jamis Buck</a> explain difficult database concepts in simple language, he does it through telling a story, and illustrates it!</p>
    <script async class="speakerdeck-embed" data-id="3b907bc997094b91ac9d578c41df8ce7" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
  </li>
  <li>
    <strong>Nothing is Something</strong>

    <iframe width="815" height="458" src="https://www.youtube.com/embed/OMPfEXIlTVE" frameborder="0" allowfullscreen></iframe>

    <p>I had the pleasure of seeing Sandi Metz speak at Burlington Ruby Conference in August, 2014 and I remember leaving pumped and inspired to code for the long haul. This time she was just as inspiring, but she also took us through some core object oriented programming concepts.</p>

    <p>But what I love about hearing Sandi speak is the way she imbues the teaching in her talks with a sense of purpose and urgency. Like DHH's talk above, I felt fired up to code. Like Jamis' talk, she made it easy to absorb complex concepts. Most of all, though, she creates this powerful undercurrent of community and warmth that makes you feel like we're all going to do this together. What an amazing teacher!</p>
  </li>
</ol>








