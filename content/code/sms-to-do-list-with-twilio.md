---
title: "SMS To Do List with Twilio"
date: 2015-08-13 19:45:40 -0400
categories: 
- Code
- Twilio
aliases: 
-  "/blog/2015/08/13/sms-to-do-list-with-twilio/"
---
The other day, I had the pleasure of talking to someone who builds mobile apps with people in developing countries so that community health workers can deliver medical information and collect data.

As were talking about the technical challenges and logistical challenges (provisioning hundreds of mobile phones and numbers in one go in a country where you have no presence, e.g.), I have a pretty clear mental model of a basic CRUD app distilled down to Android...and then he said something that changed how I thought about the entire problem:

**Some of their programs are limited to SMS-only communication.** No smartphones, no apps, just text.

<!--more-->

How do you go about guiding someone through a decision tree or collecting form submissions via SMS?

By coincidence, I had just started reading [a book about building command line apps](https://pragprog.com/book/dccar2/build-awesome-command-line-applications-in-ruby-2) and I think that's how the lightbulb went off for me.

As a developer, I spend a lot of time in front of a command prompt. Many of the more experienced devs I know wouldn't want to touch anything other than the command line to do the bulk of their work -- **and they are navigating an application interface largely built around entering a single text command at a time**, just like our SMS-constrained health workers.

In *Build Awesome Command-Line Applications in Ruby 2*, one of the first sample projects is a to do list app, from the command line.

Your basic set up allows you to add items to the list, retrieve the whole list, and mark items as complete. As I was building it out, I also wanted to delete things, because I found that more satisfying.

Once the idea of an interactive SMS app and the command line to do list fused in my head, I thought it would be fun to write a simple, somewhat interactive program that was all SMS-based.

Twilio for Easy SMS Integration
-------------------------------

Twilio is a service that allows you to send and receive voice and SMS through their API. They have awesome documentation for a bunch of different languages and great small project tutorials like the one I was about to tackle.

I stumbled across [this one about sending out baby announcements](https://www.twilio.com/blog/2014/10/broadcast-text-and-picture-messages-using-ruby-google-spreadsheets-twilio.html) as I was working and I found it very useful. I was all on board with the google-sheets-as-backend until I got past reading and started trying to write to the sheet. That was too complex for this little project!

**Diving into Twilio, all I had to do was set up a web endpoint to receive messages and write some simple code to generate a reply.** That's it, one controller action!

Here's what I used:

- [Set up twilio and Rails](https://www.twilio.com/blog/2014/02/twilio-on-rails-integrating-twilio-with-your-rails-4-app.html)
- [Get your local endpoints online with Ngrok](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html)
- Write your application logic in the Rails app, just like you were receiving and responding to any normal web request

It really is that easy to get started. In all honesty, I did try to poke at the problem from a non-Rails angle for a little bit at first, but I wanted to focus on the Twilio side of things instead. Note to self: I'm getting too comfortable with Rails conventions!

One Web Endpoint
----------------

Here's the controller I wrote to handle incoming messages from the Twilio API and respond with TwiML, Twilio's own version of XML:

```ruby Message Controller
class MessagesController < ApplicationController
  def index
    initialize_command(params)
    twiml = Twilio::TwiML::Response.new do |r|
      r.Message @command.execute ? @command.response : 'Sorry something went wrong'
    end
    render text: twiml.text
  end

  private

  # build a message and command from incoming params that can be executed to deliver the response
  def initialize_command(message)
    message = Message.new(params)
    @command = begin
      "#{message.command.capitalize}Command".constantize.new(message)
    rescue
      HelpCommand.new(message)
    end
  end
end
```
The twilio-ruby gem give you wrappers for the response object, so there's not a lot of heavy lifting to be done.

Responding to Commands
----------------------

In command line apps, you get a limited number of valid options and a rigid structure to follow when you're executing commands -- something along the lines of [command] [flags] [arguments].

Here, I wanted to follow a similar convention, at least as far as separating the commands from the message that was being sent.

When I talked to app developer about SMS-based form submission, he said they basically rely on the same thing. **You have to develop a convention for setting apart your commands or your form field identifiers from the data that is being sent.**

We serialize data for web requests all the time, the only difference is that here we need to guide the user into compliance with those conventions because they just have a big text box.

For starters, I decided that I would:

- adopt a convetion of commands coming first, surrounded by * characters on each side, followed by the message
- use "help" command as a catch-all to rescue any user input that didn't follow the command/message convention
- write helpful, specific prompts for each valid command to ensure that a user always gets a reply and that the reply to invalid commands leads them towards valid ones

To model the command/response structure, I copied a pattern we've used often at work: start with a base class that to initialize the command objects, then create subclasses for each command that all know how to "execute" and "respond".

Inside the "execute" and "response" methods, you can then define unique behavior for each command, but in the controller code above, for example, you simple have to make calls like "command.execute" and "command.response."

So, for example, when I parse a message that looks like this

>\*new\* add something to the list

a NewCommand object is created. When it's executed, the new to do list item is saved to the database, and the response is returned, telling the user that their new to do list task has been added.

```ruby New Command
class NewCommand < Command

  def execute
   @item = Item.new(item_options)
   @item.save!
  end

  def response
    "Task added: #{@item.description}"
  end
end
```

If they want to see a list of all their items, they just need to text

>\*list\*

and the ListCommand responds with a list of their items or a prompt to add something if there aren't any items:

```ruby List Command
class ListCommand < Command

  def execute
    @list = Item.where(from: @message.from).order(:created_at)
  end

  def response
    if @list.empty?
      "Looks like you haven't added anything yet. Create a new item with *new* followed by the item description."
    else
      items = []
      @list.each_with_index do |item, index|
        list = "#{index + 1}: #{item.description}"
        if item.completed_at.present?
          list += ", (Completed: #{item.completed_at.to_date})"
        end
        items << list
      end
      items.join(', ')
    end
  end

end
```

I also built out commands to mark items as complete and remove them from your to do list. Both take integer messages that correspond to the number of the item you get back from the list command.

So this command would remove the second item on your list:

>\*remove\* 2

Debugging Twilio Apps
---------------------

One of the trickiest parts of even doing this simple app was figuring a good way to debug.

I *think* Twilio has some sandbox features, but at $00.0075 per message, I wasn't too concerned about cost. It was more an issue of figuring out the best way to test input, return values from methods and objects, and visualize the whole request/response cycle, since it is different than the usual web flow I'm used to.

A couple of things I found helpful:

- Creating a view to render the response for the controller, so instead of sending the response back to the texter through Twilio, I could view and debug output locally in the browser
- Reading the Twilio error logs -- they have very clear inbound and outbound message logs that give you insight into the headers, parameters, and bodies of the requests and responses in your app
- [to_query](http://apidock.com/rails/ActiveSupport/CoreExtensions/Hash/to_query) to turn params hashes into query strings that I could add to my urls in the browser during local testing, especially because this is a typical incoming request query string:

> /messages?ToCountry=US&ToState=MA&SmsMessageSid=SMe40c71a5a09f1bad9ff702fce90b1d9d&NumMedia=0&ToCity=ROXBURY&FromZip=1096&SmsSid=SMe40c71a5a09f1bad9ff702fce90b1d9d&FromState=MA&SmsStatus=received&FromCity=BOSTON&Body=*list*FromCountry=US&To=8573992266&ToZip=1097&NumSegments=1&MessageSid=SMe40c71a5a09f1bad9ff702fce90b1d9d&AccountSid=AC428abc24c52ac55ff5cd98b68bd6a5e7&From=7811234567&ApiVersion=2010-04-01

Check out the Code
------------------

If you want to see more, [here's the code](https://github.com/dankleiman/sms_todo).
