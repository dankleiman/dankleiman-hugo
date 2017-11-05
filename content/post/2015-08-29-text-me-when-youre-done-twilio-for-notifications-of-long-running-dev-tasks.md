---
title: "Text Me When You're Done: Twilio for Notifications of Long-Running Dev Tasks"
date: 2015-08-29 10:33:48 -0400
categories: 
- Code
- Twilio
aliases: 
-  "/blog/2015/08/29/text-me-when-youre-done-twilio-for-notifications-of-long-running-dev-tasks/"
---

This week at work, we ran into a slight hiccup with one of our larger third-party data syncs. Without going into too much detail, to fix the issue, we had to carefully reproduce data in various states and test fixes that would transform that data back to the correct state -- or for the purpose of this post, *I spent a lot of time this week setting things up and waiting for them to run*.

Outside of work I've been continuing to play with Twilio and this morning, with hours of data prep still in front of me, I stumbled across this article on [Sending a Twilio SMS from the Shell](https://www.twilio.com/labs/bash/sms).

<!--more-->

Before I get into how this works and what I did, I was also reading some of Patrick McKenzie's old posts on his first Twilio apps. What got me excited this morning was [something he wrote as an addendum to his TwilioConf talk](http://www.kalzumeus.com/2011/12/19/productizing-twilio-applications/).

I now consider it my mission statement for all my Twilio projects:

> ## Why I Think Twilio Will Take Over The World
>
>
>(This was not actually in the presentation, because I didn’t have enough time for it, but I sincerely believe it and want to publish it somewhere.)
>
>I think Twilio is, far and away, the most exciting technology I’ve ever worked with. The world needs cat photos, local coupons, and mobifotosocial games, too, but it needs good telephony systems a lot more, as evidenced by companies paying billions of dollars for them.
>
>Additionally, Twilio is the nascent, embryonic form of the first Internet that a billion people are going to have access to, because **Twilio turns every phone into a smartphone**.  The end-game for Zynga’s take-over-the-world vision is the human race slaved to artificial dopamine treadmills.  The endgame for Twilio’s vision is that every $2 handset in Africa is the moral equivalent of an iPhone.  I know which future I want to support.
>
>Smartphones aren’t smart because of anything on the phones themselves, they’re smart because they speak HTTP and thus get always-on access to a universe of applications which are improving constantly.  Twilio radically reduces the amount of hardware support a phone needs to speak HTTP — it retroactively upgrades every phone in the world to do so.  After that, all you need is the application logic.  And what application logic there is — because the applications live on web servers, they have access to all the wonderful infrastructure built to run the Internet, from APIs that let you get Highly Consequential Data like e.g. weather reports or stock prices or whatever, to easy integration with systems which were never built to have a phone operating as part of them.
>
>You can’t swing a stick in a business without hitting a problem which a phone application makes great sense for.  I filled up three pages of a notebook with them in just a week after being exposed to Twilio for the first time.  Order status checking for phone/fax/mail orders.  Integrated CRMs for phone customer service representatives.  Flight information.  Bank balances.  Server monitoring.  Appointment reminders. Restaurant reservations.  Local search.  Loyalty programs.  Time card systems.  Retail/service employee support systems.  Shift management.  The list goes on and on and on.
>
>Seriously, **start writing Twilio apps**.

Thanks, Patrick!

Twilio SMS via Shell
--------------------

Up to this point, I had been thinking of Twilio as a way to tie SMS, either as input or output, to web-based application logic. When I came across the shell script that would also hit Twilio to send SMS, though I realized that chaining a Twilio SMS to a long-running script would allow me to set up and job and just walk away. I'll get a text when it's done. Awesome!


At it's core, the script is a curl request to the Twilio API:

```bash
RESPONSE=`curl -fSs -u "$ACCOUNTSID:$AUTHTOKEN" -d "From=$CALLERID" -d "To=$PHONE" -d "Body=$MSG" "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNTSID/SMS/Messages" 2>&1`
```

The rest of the script takes care of arguments and configuration -- even allowing you to create a separate config file with your Twilio credentials. Pretty sweet to have such a nice neat package! [Here's everything you need to get it running](https://www.twilio.com/labs/bash/sms)

Integrating Tasks with the Script
---------------------------------

I've played with a few different alerts so far.

When I had to load a large file full of sql data, a simple alert when the job was done did the trick:

```
mysql -u root databasename < some/file.sql; echo 'Your table is ready' | ~/twilio-sms 6178675309
```

When I was deciding how to break up the file into more manageable smaller files to import, and running around doing errands and walking my dog, just calculating the number of lines took long enough that I piped the result out to the Twilio script and got a text that said 34218:

```
wc -l < some/file.sql | ~/twilio-sms 6178675309
```

There's nothing earth-shatteringly-amazing technically here. It's really about peace of mind.

Now, I don't have to keep looking over my shoulder to check if the task is done. Or waste time checking Twitter while I sit at my computer. I can go do more useful things, like finish this blog post, confident that the text notification will be enough to get my attention when the job is done running.
