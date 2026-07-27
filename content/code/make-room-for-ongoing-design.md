---
title: "Make Room for Ongoing Design"
date: 2026-07-27
description: "A whiteboard design and the system that ships from it are never the same thing. Revisiting a project well after handoff means reconstructing what actually shipped together, not grading it against the original diagram."
summary: "A whiteboard design and the system that ships from it are never the same thing. Revisiting a project well after handoff means reconstructing what actually shipped together, not grading it against the original diagram."
tags: ["software engineering", "software architecture", "technical leadership"]
categories: ["code"]
---

A few weeks after we shipped the first version of an identity-resolution pipeline, I sat down with the project lead to review what we had built.

Customer data arrives from many sources, often with partial or conflicting information. That can leave us with an incomplete picture of how a customer has interacted with a business. The system was designed to detect when two customer profiles represent the same person, so we can merge their attributes and event history.

For example, someone types gnail.com instead of gmail.com into a form, then uses the correct address when they place an order. Our steel thread was to detect common email domain typos and match them to profiles with the correct one. Those simple deterministic rules let us build the matching, merging, and audit pipeline end to end.

We knew more sophisticated matching rules would follow. Our data science team was developing probabilistic matching based on partial matches for names, addresses, and other behavioral signals. Businesses also wanted a way to supply matches of their own. The processing pipeline should be able to work with any incoming match.

The project lead and I investigated the data, drew the components up on a whiteboard, and worked through the initial design together.

Then he took it to the team to build.

## Delivery Changes the Design

No design ships exactly the way it gets drawn up on a whiteboard.

Once the lead started implementing the system, he had to answer questions that never came up during the initial design.

How should the jobs process large batches efficiently? What state should we track on each profile? How would a customer validate a match? What information would the application need to render?

By the time I checked in, typo detection was working in production, but the boundaries between the system's components had changed. The team had made dozens of small choices to solve problems that only appeared during implementation. Each one shifted the design slightly.

## Walk Me Through Your System

Whenever I come back to a project I helped design but haven't followed day to day, I'm cautious. I still remember the clean version we drew on the board, but the project lead knows what it took to make that version work in production.

From a distance, every difference between the current system and the one we designed sticks out. It's tempting to swoop in and rattle those off and ask "what did you do to my system?"

The reality is that the production system is no longer my whiteboard design. It contains the constraints, discoveries, and compromises required to make it real.

More importantly, I want the team lead to own this system and its evolution over time. I can't play architecture gatekeeper and hand off ownership at the same time.

Instead of asking about "my design," I start the conversation with, "Walk me through your system."

## Reconstruct What Actually Shipped

This is not a conversation to squeeze into a 30-minute status check.

High-level architecture comments thrown out in a status meeting just become more action items on the delivery checklist. Shaping the system requires a different kind of conversation.

We scheduled a separate, open-ended architecture session. At the whiteboard, the lead walked me through the whole data flow as it existed in production.

How did the matching job operate? What happened after it found two profiles? Where did we record match history? How was the match validated? How did the result become visible in the UI?

We drew the path from raw profile data through matching, processing and serving to the application. Then we worked backwards from those details and redrew the responsibilities around them.

The implementation details stopped being mistakes or accidents. They became design choices we could examine together.

This time we were designing production evidence. Typo-detection was already running and we had sample probabilistic matching cases to work with.

A probabilistic model would produce two profiles, a reason for the match, and a confidence score. The business could decide what confidence level was strong enough to merge on. After that, the match should enter the same processing pipeline as one produced by a deterministic typo rule.

As we ran that case through the production system, some parts fit cleanly. Other parts exposed places where typo detection and match processing had become too tightly coupled.

## The Fix Was Small

The change we landed turned out to be small. We adjusted the metadata that represented why a match had occurred and its validation status. With that small change, deterministic typo matches and probabilistic matches collapsed into the same interface.

The design had moved away from the original diagram, but that was ok. Running the next use case through the system showed us which original boundaries still mattered and helped us find a small tweak to preserve them.

At the end of the conversation, the lead said something that stayed with me:

> I've been so heads down in all the details. I haven't had time to think about the problem this way since we did the initial design.

He had been tuning batch jobs, tracking state, and connecting the processing pipeline to the product experience. That was the work required to ship to production.

## Teach the Pacing

Over time, our software systems require both kinds of work. Sometimes the right thing to do is stay heads down and ship. Sometimes the next small decision is about to become a permanent architectural choice.

I want our leads to develop a feel for those shifts. At first, I might need to create those moments for them, but the goal is for the leads themselves to start calling for the design session or to tell me, "No, that can wait. I need another week of focused implementation."
