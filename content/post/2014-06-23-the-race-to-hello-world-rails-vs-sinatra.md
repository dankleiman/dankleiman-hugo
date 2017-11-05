---
title: "The Race to Hello World: Rails vs. Sinatra"
date: 2014-06-23 08:11:28 -0400

categories: 
- Code
- Rails
- Sinatra
aliases: 
-  "/blog/2014/06/23/the-race-to-hello-world-rails-vs-sinatra/"
---

Earlier, I explained how I built [my personalized url shortner](/blog/2014/05/30/buying-a-mongolian-website/) in Sinatra.

This past week, we've been spinning up demo apps in Rails instead, so I wanted to walk through a little comparison of the two frameworks.

As [one of our instructors](https://github.com/radavis) said, "Sinatra is like a stripped-down muscle car and Rails is like an RV."

Here's how setting up a simple "Hello, World!" app breaks down between the two.
<!-- more -->

Sinatra Set-Up
--------------

To set up, "Hello, Sinatra" from the command line, follow these steps:

1. $mkdir sinatra_hello
2. $cd sinatra_hello
3. $gem install sinatra
4. $touch app.rb
5. In your app.rb file, add:

```ruby

require 'sinatra'

get '/' do
  "Hello, Sinatra!"
end

```

To see the locally running version, start the app with ruby app.rb and visit http://localhost:4567.

Rails Set-Up
------------

From the same directory we started in, instead of creating the new directory like we did for sinatra, we will follow these steps:

1. $rails new rails_hello
2. $cd rails_hello
3. $rails generate controller Posts
4. Add an index method to posts_controller.rb
5. define the root path in config/routes.rb to be 'posts#index'
6. create a view for the root route that says 'Hello, Rails!'

Now, when we start up the rails server from the command line, we can visit http://localhost:3000 and see our 'Hello, Rails!' message.

Simplicity vs. Structure
------------------------

As you can see from the code above, you need to install one gem and edit one file in your Sinatra version to get the basics working.

In that one file, you tell the server what to do with one HTTP 'GET' request: where to go and what to display.

In contrast, in Rails, directing the request and displaying the response are delegate to different areas of the application:

- routes.rb interprets the 'GET' request and sends us to the Posts Controller
- inside the controller, there are instructions for what to do with the request for "index"
- a specific view file (app/views/posts/index.html.erb) finally configures the response: "Hello, Rails" printed to the page.

We were fortunate to work with HTTP requests a little more directly in Sinatra first, before we started relying on the conventions of Rails to more "magically" handle them for us.

At first, learning Rails feels like learning what files to put where to make the right thing happen.

When we worked out of a single server file in Sinatra, in contrast, we were tracking the different components of HTTP requests and responses more directly.

Coming away from these last two weeks of playing with Sinatra and Rails, I'm glad we started with Sinatra for the directness, but I can also see, as our projects get bigger, how the conventions and structures of Rails will allow us to maintain clear, organized code.



