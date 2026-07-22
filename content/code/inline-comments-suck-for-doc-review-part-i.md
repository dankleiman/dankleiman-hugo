---
title: "Inline Comments Suck for Doc Review, Part I"
date: 2026-07-21
description: "Comment threads on a design doc create a false sense of progress. Real design review means treating comments as signals to synthesize into decisions, not a checklist to clear one thread at a time."
summary: "Comment threads on a design doc create a false sense of progress. Real design review means treating comments as signals to synthesize into decisions, not a checklist to clear one thread at a time."
tags: ["design docs", "engineering management", "writing"]
categories: ["code"]
aliases: ["/code/inline-comments-suck-for-doc-review/"]
---

Writing a technical design document is supposed to help teams arrive at a sound engineering decision.

When you share your design doc with other teams, it gets peppered by inline comments and you resolve the comment threads one at a time. The comment resolution loop creates a sense of progress. Comments arrive. You respond. Threads disappear. The document gets cleaner.

But notice what happens when everyone gets together to review the final version? Nobody wants to walk through the comment threads one by one. Combined synchronous time is expensive. The team stops pretending that every comment deserves equal attention.

Instead, the moderator asks:

- What actually remains undecided?
- Which concerns still matter?
- Where are reviewers talking past one another?
- What evidence is missing?
- What changed enough to invalidate an earlier conclusion?

In the expensive live meeting, the group immediately abandons the point-for-point comment-based workflow.

Technical decisions improve iteratively. A design doc should be a malleable artifact, just like code being shaped through PR review. But comment-based editing workflows create a trap. Every comment becomes a task and you either answer, edit, or resolve it. Unfortunately, handling comments one by one is the path of least resistance with these tools. Driving towards a better technical outcome requires deliberate effort above and beyond the tool's happy path.

## Stay out of the Comment Stream

When you share a doc for review, your colleagues will start to read and respond with comments. These comments come in, one by one as people are processing what they are reading.

A stream of incoming comments means that people are reading your work and thinking about it and you want to be responsive to that. But responding to new comments is the first trap. If you go point-for-point as comments arrive a few anti-patterns will take over.

First, they haven't completed their read of the document. Reviewers will often leave a question and then realize the document answers it a few paragraphs later. When you respond to comments as they arrive, you're addressing incomplete thoughts so you risk missing a deeper core concern.

Responding too quickly also makes it harder for patterns to emerge across reviewers. Maybe multiple people point out related issues that all come from a flaw in the overall design. They might each be pointing out a small part of it that impacts their systems, but if you address each comment in a separate thread reactively, you can miss the connection.

What's worse is that by responding to independent threads, it's harder for each commenter to see the big picture as well. These are the kinds of things that become clear when everyone gets in a room together, but you are fighting your tools if you want to drive this collective insight earlier and asynchronously.

Comments are signals, not tasks. Your job is to interpret those signals, figure out the concerns underneath them, and act more like the live meeting moderator throughout the review, not just when everyone finally gets into a room.

## Set Expectations to Get the Best Feedback

Imagine you present your doc for feedback. You're hoping to get alignment on the problem statement, but haven't asked for that explicitly. Someone will read your draft and start debating the typing in an API signature. If the problem statement changes and that API gets thrown away, that reviewer has wasted a whole review cycle.

Without clear guidance on what kind of review you are looking for from each reviewer and what the overall stage of the design is, people will guess or assume. Once again the tools — a doc with the ability to comment on it — don't help guide the right behavior. It turns out, many people are happy to comment away in a vacuum anyway.

Your job as the moderator begins before the first comment. Design iteration happens in phases and you have to create clear signposts about what phase the review is in and what kind of feedback you need.

When you share the doc, tell reviewers:

- Which decisions and questions are open.
- What research, testing, and prototypes support the current proposal.
- What kind of feedback would be useful.
- What is out of scope for this review phase.

## Compress Feedback into Decisions

Acting as a moderator means resisting the pull of the comment-response loop.

A good moderator treats each comment as a signal that something interrupted the reviewer's understanding or confidence. You need to focus on understanding where the interruption is coming from.

Is the reviewer confused by the explanation? Challenging an assumption? Applying a different constraint? Pointing to an architectural flaw? Reacting locally to a problem that affects the whole proposal? Does their confusion show up in other comments, implying a larger pattern?

Separate comments about retries, partial failures, recovery, ownership, and on-call burden may point to a central issue: "Can this system be operated safely when one participating service is unavailable or returns partial results?"

Building confidence in the operational health of the system becomes a different engineering exercise than answering each smaller concern in isolation.

The answer may require a design change. It may require a prototype, production data, an ownership agreement, or a narrower scope. The right response depends on the diagnosis.

As a moderator, you should:

- Connect related reactions.
- Distinguish local confusion from structural disagreement.
- Expose incompatible goals and constraints.
- Identify the questions most blocking the decision.
- Decide what evidence or work would resolve them.
- Keep the review focused on those questions.

This is very different from answering comments one by one as they come in.

## Keep Continuity as the Design Changes

A good review process often changes the proposed design significantly. While getting to a better technical solution is a good thing, the change of direction creates a new problem for you as the author.

When a reviewer who saw the first version comes back and starts reading again, they may find a different architecture, rewritten sections, and orphaned comments. Why did this change? The doc gives them no obvious explanation, so they have to comb through resolved comment threads and version history.

As an author, you have very limited breadcrumbs to leave your readers by default with these tools. The version history for text changes is not a decision history that explains why something changed or how the design is evolving in response to feedback and discovery.

Every time the design moves forward, you need to bring the team along. You have to capture the important changes and explain why they happened, tracing them back to the original concerns that were raised. Do the work of figuring out how the changes impact other assumptions and make sure the reviewers know what to re-review.

A version history shows how the document changed. You have to preserve how the decision changed.

## Act as the Moderator from the Start

Scarce synchronous meeting time acts as a forcing function. The moderator cannot afford to treat every comment or concern equally. They cut off low-value discussion, surface the most important disagreements, and focus the group on making decisions.

As the author, you should apply the same discipline from the start. At every stage of the process, keep asking which questions matter most, what evidence is missing, and what work would actually move a decision forward.

You won't be able to control how reviewers provide feedback, but you can set the pace for how the team works through that feedback and prevent the comment loop from driving the process.

Run the moderator loop:

- Set the level of the review.
- Treat comments as signals and synthesize them into decisions.
- Make the design evolution clear and accessible.

Act as the moderator from the moment you share the document, not just when everyone gets together at the end.

That discipline is only half the fix. The other half sits with whoever's leaving the comments. In [Inline Comments Suck for Doc Review, Part II](/code/inline-comments-suck-for-doc-review-part-ii/), we flip the vantage point and look at what it takes to review a design doc well.
