---
title: "Inline Comments Suck for Doc Review, Part II"
date: 2026-07-22
description: "Leaving a comment every time something catches your eye feels like a thorough review, but it just hands the author a pile of reactions to organize. Here's how to review like you're helping drive a decision, not narrating your read."
summary: "Leaving a comment every time something catches your eye feels like a thorough review, but it just hands the author a pile of reactions to organize. Here's how to review like you're helping drive a decision, not narrating your read."
tags: ["design docs", "engineering management", "writing"]
categories: ["code"]
---

In [Inline Comments Suck for Doc Review, Part I](/code/inline-comments-suck-for-doc-review-part-i/), we looked at the limits of comment-based editing workflows from the author's perspective. Now flip the vantage point: you're the reviewer, and the same tools that trap the author in a comment-response loop can trap you into producing a stream of reactions instead of a review.

You open a design document and start reading.

A sentence raises a question, so you highlight it and leave a comment. A few paragraphs later, an assumption looks wrong. You leave another one. Then you find an API choice you would have made differently.

Highlight. Comment. Continue.

By the time you reach the end, the document contains a detailed record of your reading experience:

- Questions you formed before seeing the next section.
- Temporary confusion that eventually resolved itself.
- Several comments that express parts of the same concern.
- A structural objection attached to whichever sentence happened to trigger it.
- Suggestions based on a path you no longer support.

This feels like a thorough review. You noticed things. You asked questions. You left evidence that you engaged with the proposal.

But on the other side of your comment stream, the author now has a lot of work to do to piece everything together.

Which comments matter? Which ones belong together? Are you asking for clarification, challenging the design, or volunteering to help change it? Does one comment block the path, or did five comments all come from the same smaller concern?

The happy path of comment-based review tools is to capture what catches your attention. There's no mechanism that turns a stream of comments into a useful review.

As a reviewer, your job is not to return everything you noticed about the doc. It is to help the author make a better technical decision with the support of your expertise.

## Find the Author's Decision

You have to approach a design doc as the visible surface of work that is being shaped.

When an author shares a draft, they are working toward a technical decision. They may be clarifying the goal, comparing approaches, discovering constraints, choosing system boundaries, or working out how several teams will divide the problem.

Before you start leaving comments, you need to pinpoint the decision the author is trying to make:

- What goal is the proposal trying to achieve?
- What is the team deciding now?
- Which questions remain open?
- What has already been decided?
- What is deliberately out of scope?
- Why were you asked to review this?
- Where does your expertise matter?

Otherwise, you will contribute at the wrong level.

You will debate API typing while the team is still choosing the system boundary. You will polish wording while two architectural paths remain open. You will propose a future abstraction during a review intended to validate the smallest viable scope.

Sometimes your expertise tells you that the stated phase is wrong. You may discover that the goal cannot be met under the current assumptions, that the proposal skipped a necessary decision, or that a supposedly settled boundary will not work.

Raise that.

Figuring out the author's current decision does not mean accepting its framing. It means understanding the work well enough to push it in the right direction.

## Help Drive in the Right Direction

The author is trying to answer a question larger than any individual comment: How are we actually going to achieve this outcome?

The author is responsible for getting there by exploring possible routes, weighing competing constraints, connecting several domains, and leading the proposal down a viable path.

You can help them navigate.

You may understand the storage access pattern, the migration path, the operational failure modes, or the cost imposed on a dependent team. You may know that an apparently simple interface requires a new ownership model. You may even see that the proposal is solving the wrong problem.

You might validate the current direction, rule out an overly complex or expensive option, or resolve a question no one else can answer.

## Don't Make the Author Guess

The author is building one decision from several reviewers' input. To make yours useful, it has to be clear what kind of input it is.

| Type of Input | What you contribute | How it supports the decision |
| --- | --- | --- |
| Clarification | Identify a local ambiguity | Remove uncertainty without reopening the larger design |
| Decision-relevant concern | Connect an observation to a requirement, claim, or goal | Show where the proposal's reasoning may need to change |
| Expert judgment | Give a conclusion from specialized knowledge | Supply a domain constraint the larger decision must account for |
| Joint exploration | Help resolve uncertainty or compare alternatives | Develop an answer that no one has yet |
| Delegated design | Take or request ownership of a bounded design problem | Let the proposal advance without forcing the author to prescribe every boundary |

Make it clear whether you are requesting an explanation, ruling out the current path, asking to work through alternatives, or identifying work that needs an owner.

Naming the contribution tells the author what you are doing, but they also need enough of your context to understand why.

## Make Your Expertise Usable

You may understand immediately why an access pattern is dangerous or why a migration estimate is unrealistic.

The author may not share that context.

A useful comment gives the author enough context to steer the larger decision.

Don't just say:

> This requires a new API.

Frame the context that the author doesn't have:

> This path requires my team to expose a new bulk API. That introduces a cross-team dependency and an access pattern the service does not currently support. Our team would need to evaluate that boundary before this option can be treated as viable. Is that investment justified by the outcome, or should we prefer a path with a lighter dependency?

Now the author can see the hidden complexity and understands which teams need to contribute to the implementation for this option.

Not every useful contribution has an obvious sentence to land on. If you have larger concerns like questioning the problem statement, the ownership model, or the system boundaries, try not to scatter them across comments on arbitrary text. Put your feedback somewhere visible and call it out as high-level, then use inline comments to point to the evidence.

Be equally clear about your own role. "We should work through this together" commits you differently from "This needs investigation." If the path needs an owner and you are not volunteering, say that too.

Ultimately, the author still owns the outcome. Your job is to give them a contribution that builds momentum towards that outcome.

## Give the Author a Review, Not a Comment Stream

Remember, if you follow the tool's happy path and publish your reading process, you shift the burden onto the author to organize your thinking.

Help your teammate out. Give the author something more considered: what you can see from your area of expertise, how it affects the proposal, and how you can help.
