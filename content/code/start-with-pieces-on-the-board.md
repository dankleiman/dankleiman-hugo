---
title: "Start with Pieces on the Board"
date: 2026-07-26
description: "LLMs make it possible for one person to prototype several plausible end-to-end designs before a cross-team feasibility conversation starts, turning a blank whiteboard into a concrete comparison of trade-offs."
summary: "LLMs make it possible for one person to prototype several plausible end-to-end designs before a cross-team feasibility conversation starts, turning a blank whiteboard into a concrete comparison of trade-offs."
tags: ["software engineering", "AI", "software architecture", "engineering planning"]
categories: ["code"]
---

In [Feasibility Is Not Estimation](/code/feasibility-is-not-estimation/), we looked at why ambitious engineering projects need work up front before design, and especially estimation.

When a project crosses multiple domains, the first unknowns are more organizational than technical. We do not yet know which teams need to be involved, where the ownership boundaries should fall, which existing systems can be reused, or how a constraint in one domain will spider out into the others.

Those are not questions a team can answer in isolation.

The goal of the feasibility work is to turn those organizational unknowns into technical unknowns. Once we have a plausible shape for the system, the engineers who own each part can tell us what is hard, what already exists, and what we have misunderstood.

In that post, I advocated for the feasibility stage to be a collaborative effort, almost like a hackathon, where we consider options seriously without becoming attached to any one. We can throw away a set of choices if we come up with a better one. The group should move fast while relying on their domain expertise to surface constraints.

When I actually ran this process for the project I described in the post, I did not do the full hackathon version at all.

I ran plausible scenarios, but I gamed them out because I wanted to be more prepared when I spoke to each tech lead one-on-one about their estimates. I was trying to minimize upfront work for them and keep them from having to load the full context just to understand the request.

## One Conversation at a Time

When I spoke to one of our tech leads, I was trying to see whether their service could play a specific role, but that role would change depending on the scenario.

I wanted to make it as easy for them as possible to slot a potential solution into a larger scenario.

For example, suppose we wanted to import historical events for a campaign. I could go to the tech lead who owned that domain and ask:

> How could historical import work?

But that puts nearly all the work on them. They have to reconstruct the broader project, imagine a design, remember the relevant constraints, and decide which part of the problem I am actually asking about.

I was having versions of this conversation across a dozen different teams, so my own familiarity with each domain varied wildly.

One technique I used was to ask an LLM to draft a sketch of a plausible change:

> Here is a PR for a historical import API that leverages the existing Create functionality. What do you think?

The sketch was not intended to be right. It was intended to make the conversation concrete.

A tech lead could look at the proposal and tell me that we would never extend the Create API that way because of a constraint I did not know about. Or they could say that the proposed API was close to something the team had wanted to build for a while, but it would make more sense to add a different capability first.

I do not think I would have gotten the same reaction by asking, out of nowhere, "How could you do this?"

Before each one-on-one, I tried to figure out the likely constraints in that tech lead's domain. I generated sketches of possible APIs, ownership boundaries, event flows, and implementation changes. Then I brought those sketches into the conversation and asked how feasible they seemed, what risks the tech lead saw, and what constraints I had failed to consider.

I was choosing the scenarios as they occurred to me. I was asking the LLM for help when I needed a more concrete version of a question. And I was the one keeping track of how the constraints spidered out across the different scenarios and affected other domains.

I had found a useful way to prepare myself for each conversation, but I was still running the design process one person at a time.

## A New Prototyping Superpower

Then I read Josh Bleecher Snyder's ["Claude Is Not a Compiler."](https://blog.exe.dev/claude-is-not-a-compiler)

It showed me a new prototyping superpower: build the same system several times, compare what the implementations decided differently, and use those divergences to discover the design questions that actually require judgment.

Once he had an initial design that seemed promising, he prompted multiple concurrent agents to implement the whole system, including tests and adversarial review. Then he asked new agents to compare the completed implementations and identify meaningful differences.

The agents had quietly made many important decisions differently. Josh worked through those divergences, experimented, and integrated what he uncovered into the final design.

His explanation of why this was possible was what made it click for me:

> LLMs now talk strategy, product, architecture, code, and machine code. It can't (yet?) do most individual tasks as well as an experienced, dedicated human, but it can do all of them, without having to schedule meetings or ask permission.

That was the new prototyping superpower. One person could steer the LLM across all of those layers and get far enough to have a serious conversation with the experts.

I had been reaching for the same research and prototyping capability from LLMs, but in a much looser way. I would take thin PRs, API sketches, demos, or sample code back to the tech leads to confirm or deny their viability. I was already comparing what each scenario exposed.

Josh helped me see that as a process we could push much further.

The problem with approaching a cross-functional design through a series of one-on-ones was that I remained the integration layer.

One tech lead would tell me about a constraint, and I would carry it into the next conversation. I would update the scenarios and try to understand how that change affected the rest of the project.

I had been using simulations to prepare myself for better conversations. Josh's process helped me see that I could build in a way that made the scenarios visible to everyone.

## Populate the Board

Before bringing the tech leads together, I could run a set of scenarios that produced richer prototypes. The goal would not be to arrive with the architecture already decided. It would be to populate the design space before everyone entered the room:

- Research the intricacies of an existing API and sketch how an import path might extend it.
- Design three possible ways to transform and replay historical events.
- Produce alternative ownership boundaries for the orchestration layer.
- Trace how each scenario would work end to end across the affected domains.
- Turn the strongest possibilities into thin PRs, API sketches, demos, or working code.

These would not need the depth of Josh's DNS implementations. They would only need to be plausible and complete enough that choices in one domain visibly affected the others.

The point is to change the opening question from:

> Okay, how do we build an account migration tool?

to:

> Here are several plausible ways this could work. What is good about each one? What breaks? What should we remix, extend, or combine?

## Play through the Scenarios Together

With several end-to-end possibilities on the board, the group can focus immediately on how the constraints interact.

A tech lead might spot a flaw in the part they own while the others show what that correction exposes elsewhere. For example, simplifying one API might complicate an event flow or shifting service ownership would add an orchestration dependency.

That is where the real feasibility work happens. The group is not evaluating each domain independently. They are comparing plausible systems and wrestling with the constraints that move across them.

This is the next experiment I want to try.

The account migration work showed me that LLM-generated scenarios could make individual conversations much more concrete. Josh's process showed me that generating and comparing those scenarios could become a deliberate stage of engineering work.

LLMs now make it practical for one person to spend a few days developing several plausible end-to-end scenarios before the group comes together.

Instead of starting with a blank board, we can jump right in to comparing constraints, tracing trade-offs, and moving the pieces around until a plausible system takes shape.
