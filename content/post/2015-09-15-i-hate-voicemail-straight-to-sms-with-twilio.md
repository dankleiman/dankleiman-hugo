---
title: "I Hate Voicemail: Straight to SMS with Twilio"
date: 2015-09-15 08:02:19 -0400
categories: 
- Code
- Twilio
aliases: 
-  "/blog/2015/09/15/i-hate-voicemail-straight-to-sms-with-twilio/"
---

I hate checking my voicemail. I hate the nagging voicemail icon on my phone that won't be dismissed unless I actually check my voicemail. I hate how listening to a voicemail, capturing relevant information from it, and calling someone back breaks up the normal flow of how I communicate with people all day long: asynchronously, via written communication like email or text.

These days, when I want to talk to someone, we plan a time to talk and that's fine. But some people still call and leave me a black-box-of-a-voicemail that I have to wade into.

I needed some way to cut voicemail out of my life...so I hooked up a Twilio app to handle it for me.

<!--more-->

No More Voicemail: Basic Flow
-----------------------------

Instead of having to call in to my voicemail, what if I could get as much relevant info as possible sent right to my phone, right away? There are probably times when actually listening to the message is necessary, so that has to be factored in too.

Here's the basic flow I set out to create:

- Someone calls and I don't answer.
- They are prompted to leave a message as they would normally expect to do.
- The message is recorded.
- The recording is transcribed.
- The transcription is sent to me as a text message, with a link to the recording.

Now I am happy, because I get just about all the information I need from a text. Plus, I have the assurance that if the transcription is incomplete, because voice-to-text is still not perfect, I can listen to the recording.

Twilio and Sinatra for Message Flow
-----------------------------------

To code this up, I used a similar set up to the [To Do List app](/blog/2015/08/13/sms-to-do-list-with-twilio/) I built earlier.

There are three main controller actions in the Sinatra app that the handle an incoming call, record the message, and then send it to me as a text:

```ruby
# incoming forwarded call
post '/calls' do
  user = User.find_by_phone_number!(params[:ForwardedFrom] || params[:CalledVia])
  Twilio::TwiML::Response.new do |r|
    if greeting = user.messages.current_greeting
      r.Play greeting.recording_url
    else
      r.Say 'Please leave a message after the beep.'
    end
    r.Redirect '/record_message'
  end.text
end

# record incoming message
post '/record_message' do
  Twilio::TwiML::Response.new do |r|
    r.Record transcribeCallback: '/messages', timeout: 30, playBeep: true
  end.text
end

# callback for incoming forwared call
post '/messages' do
  if user = User.find_by_phone_number!(params[:ForwardedFrom] || params[:CalledVia])
    # save recording url, generate pin for message
    message = user.messages.create(pin: Message.generate_pin_for(user), recording_url: params[:RecordingUrl], recording_sid: params[:RecordingSid])
    text = params[:TranscriptionText] || 'Unable to transcribe message'
    body = ["FROM: #{params[:Caller] || params[:From]}",
            "MSG: #{text}",
            "CALL TO LISTEN: +18001231234",
            "MSG PIN: #{message.pin}"].join("\n")
    client = Twilio::REST::Client.new ENV['TWILIO_ACCOUNT_ID'], ENV['TWILIO_AUTH']
    client.account.messages.create(body: body, to: user.phone_number, from: params[:To])
  end
end
```
That's it. Calls get recorded and forwarded to me and the caller leaves a voicemail just like they intended to do.

Here are a few things I learned with this new Twilio use case.

Leave a Greeting
-----------------

In the '/calls' block, instead of just the robo-voice that Twilio defaults to prompting the caller to leave a message, I wanted to be able to play a custom greeting.

When you use the Record verb in Twilio, they will save the recording for you, so I just needed to save the url that points to that resource and the unique id of the recording, in case I want to go back and clean it up later.

To allow for a custom greeting, I built a separate flow to actually record the outgoing greeting. When I call to check my message, I get a prompt that allows me to record a new greeting.

To play the greeting to my callers, I then looking up the number the call has been forwarded from and play the custom greeting if there is one.

Skinny Controllers, Really Skinny
---------------------------------

As I was building out the custom greeting, I ran into a timeout issue when playing the greeting and recording the call in the same action.

I have to look into this more, but Twilio seems to have a really small size limit on the response. Super small controller actions as a constraint makes me think that any complex application logic is going to lots of extra controller actions.

Whatever my next project is, I'll need to think about the best design to keep the Sinatra app from being tons of seeming unrelated actions.

Transcription Callback
----------------------

The '/messages' action, where the app actually sends me the text, is hit as a callback from the transcribeCallback option on Record.

This is pretty cool, because once the caller records their message, their interaction with the app is done. Twilio then takes the recording, runs the voice-to-text transcription, and posts the attributes of the transcription to '/messages'.

From the [Twilio API Record docs](https://www.twilio.com/docs/api/twiml/record), you get the following parameters in the callback:

- TranscriptionSid: The unique 34 character ID of the transcription.
- TranscriptionText: Contains the text of the transcription.
- TranscriptionStatus: The status of the transcription attempt: either 'completed' or 'failed'.
- TranscriptionUrl: The URL for the transcription's REST API resource.
- RecordingSid: The unique 34 character ID of the recording from which the transcription was generated.
- RecordingUrl: The URL for the transcription's source recording resource.
- CallSid: A unique identifier for this call, generated by Twilio.
- AccountSid: Your Twilio account id. It is 34 characters long, and always starts with the letters AC.
- From: The phone number or client identifier of the party that initiated the call. Phone numbers are formatted with a '+' and country code, e.g. +16175551212 ([E.164][e164] format). Client identifiers begin with the client: URI scheme; for example, for a call from a client named 'tommy', the From parameter will be client:tommy.
- To: The phone number or client identifier of the called party. Phone numbers are formatted with a '+' and country code, e.g. +16175551212 ([E.164][e164] format). Client identifiers begin with the client: URI scheme; for example, for a call to a client named 'jenny', the To parameter will be client:jenny.
- CallStatus: A descriptive status for the call. The value is one of queued, ringing, in-progress, completed, busy, failed or no-answer. See the CallStatus section for more details.
- ApiVersion: The version of the Twilio API used to handle this call. For incoming calls, this is determined by the API version set on the called number. For outgoing calls, this is the API version used by the outgoing call's REST API request.
- Direction: A string describing the direction of the call. inbound for inbound calls, outbound-api for calls initiated via the REST API or outbound-dial for calls initiated by a <Dial> verb.
- ForwardedFrom: This parameter is set only when Twilio receives a forwarded call, but its value depends on the caller's carrier including information when forwarding. Not all carriers support passing this information.

Checking Messages
-----------------

Once the message comes through, I get a text with a (hopefully) coherent message, and a fallback option to call in and listen to the record.

Right now, I have the very *cough cough* secure combination of a "from" phone number and "message PIN" to authenticate against in order to play the message.

It's going to be interesting to think more about securing Twilio-related resources in future projects, but for now, this seems to work.

So call me. Or don't. I can handle it either way now!
