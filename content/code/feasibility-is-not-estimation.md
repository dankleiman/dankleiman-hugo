---
title: "Feasibility Is Not Estimation"
date: 2026-07-24
description: "Rolling up team estimates for an ambitious cross-team project hides the architectural choices behind them. Real feasibility work means simulating how the pieces fit together before anyone estimates."
summary: "Rolling up team estimates for an ambitious cross-team project hides the architectural choices behind them. Real feasibility work means simulating how the pieces fit together before anyone estimates."
tags: ["software engineering", "software architecture", "engineering planning", "technical leadership"]
categories: ["code"]
---

Recently, I was asked to assess the feasibility of a new account migration tool.

I was operating in a familiar tech lead role: leadership wanted an answer about whether the project was worth pursuing, while the teams involved needed enough technical definition to understand what they might actually have to build.

At first, the request sounded straightforward. We went to each engineering team and asked:

> What would you need to support account migration?

The answers came back all over the map.

One team thought it needed a pair of export and import APIs. Another imagined a compatibility layer so old account IDs would continue to work. Someone else started describing an orchestration service that would coordinate migrations across every domain.

One team assumed we would move all of the account's historical data. Another assumed we would move only active configuration and customer profiles.

The estimates did not look remotely comparable.

At first, this looked like the familiar problem of engineers racing ahead on shaky requirements. Teams were making different assumptions, and some people were probably overestimating while others had not thought through their edge cases.

We clarified the requirements, tightened the estimates, and shared them with leadership.

But here's where things fell apart even more.

Once those estimates left the teams that produced them, the context behind each number disappeared. Even though we tried to get more specific about the requirements, teams still pictured different architectures for the tooling. Those differences changed what each team assumed about its own role and how other services would work.

There was no point in the process where we tested those assumptions together. When we handed off the estimates, leadership saw one team with two weeks of work and another estimating nine months, but both numbers appeared to describe the same request. The conversation naturally shifted from "Can we build this tool?" to "Why are these estimates so different?"

## Answering the Wrong Question

Tech leads are often asked questions like this and it's tempting to respond as though they were *implementation* questions. If you get asked, "can we consolidate these platforms?" the real question is rarely "can this team build an API that connects system A to system B?"

Leadership wants to know whether there is a credible path from the organization's current systems and capabilities to a desired outcome. That outcome-focused perspective matters because feasibility for an ambitious cross-team initiative is not just technical.

Ownership may be unclear. Security constraints may invalidate the workflow. Legal requirements may change what data can move. Operational recovery may require capabilities nobody owns. Customer expectations may conflict with the way the underlying systems work.

The question is not only whether each team can build its piece. It is whether the organization's systems, teams, constraints, and capabilities can be arranged into a coherent approach at all.

Even if we limit our focus to the engineering work, most engineering projects do not carry the same kind of uncertainty as broad cross-team efforts.

## Uncertainty Lives Between Domains

Ask a team to extend an existing service with another API, and it can draw on years of experience running that service. The implementation pattern is familiar. There are unknowns like new edge cases, scaling concerns, testing, and rollout, but the team has solved problems shaped like this before. It can estimate from experience.

Ambitious cross-team initiatives are uncertain for a different reason. The uncertainty does not live inside any one component.

Every team recognizes its own piece.

We've replayed events before. We know how to build an import API.

None of the components is especially mysterious. The uncertainty lives between those capabilities. Can they work together? Where do their assumptions conflict? Does one new capability unlock the entire approach, or expose five more things the organization does not know how to do?

Confident estimates of familiar components cannot be added up into an estimate of a new system when the pieces have never been put together this way before.

That is exactly what had happened with reporting consistency in the migration tool project.

Customers needed to keep reporting on historical campaign performance after moving to the new account, with as little disruption as possible. Presented as a single requirement, though, reporting consistency gave teams room to interpret the implementation in several different ways.

The reporting team estimated a permanent mapping layer that could translate old campaign IDs to new ones across reporting surfaces.

The campaigns team designed a historical backfill that would recreate campaigns while preserving their original IDs.

The events team was considering whether historical events should be transformed during migration. If campaigns received new IDs, then the events pointing to them would also need to be rewritten so that reporting wouldn't lose the ability to aggregate old campaign data.

Each team had arrived at a solution inside its own domain with reasonable assumptions about the rest of the system.

The problem was that those solutions described different systems.

## Work the Possibilities Together

In retrospect, I wish I had framed the "feasibility" stage of the process more like a hackathon.

A good hackathon asks people to collaborate intensely enough to make an idea tangible without pretending the result is production-ready. People leave their domain boundaries, follow promising ideas, and discover things that would remain hidden in isolated work. The prototype may be thrown away, but the group learns something valuable.

For the migration project, I would have brought the core group together, explained that we were not estimating or endorsing a design, and timeboxed the exercise around playing several possible scenarios out all the way through.

Suppose historical campaigns are recreated in the destination account with their original IDs. That may preserve the references on existing events, but can the campaign system safely recreate those identities? What other account-scoped data depends on them?

Suppose campaigns are recreated with new IDs instead. That may be easier for the campaigns system, but now historical events refer to the wrong records. Do we rewrite millions of events during migration?

Suppose we leave both the campaigns and events alone. Now reporting needs a permanent mapping layer that translates identifiers whenever customers query historical performance. Which reporting surfaces need that logic, and who operates it indefinitely?

All three approaches could preserve reporting consistency. Each moved the difficult work into a different domain.

Nobody was in a position to pick one of these scenarios as the design up front. The campaigns team could evaluate the cost of preserving identifiers, but not every consequence of rewriting events. The events team could reason about a historical transformation, but not the permanent complexity added to reporting if we avoided it. The reporting team could estimate a mapping layer, but that estimate said nothing about whether introducing one across every reporting surface was a good system-level choice.

Asking every team to fully estimate all three approaches would multiply divergence and create redundant planning work.

Take one scenario seriously enough to expose its dependencies, failure modes, and missing capabilities, but hold it loosely enough to abandon it when it stops making sense. Follow it far enough to see where the work moves and whose knowledge the next pass requires, then repeat with another.

When I did get into this mindset with people, playing through the scenarios changed the conversation. Teams stopped describing projects they might need to build in abstract terms and started making connections to capabilities they already understood.

The exercises didn't magically prove that migration tooling would be easy to build, but it made several possible approaches concrete enough to compare.

## Let the Simulation Find the Right Participants

A shared simulation also changes who needs to participate.

The reporting-consistency constraint did not belong to one team. Following it through connected campaign creation, event transformation, identifier management, and reporting behavior across several domains. Each branch exposed another domain whose constraints could change whether the approach worked.

That does not mean inviting everyone who might eventually be affected. Expand the group as the constraints of the problem expand.

Start with the people who understand the capabilities and constraints already visible in the scenario. Play it through until the group reaches a question it cannot answer, then bring in the person who can represent that constraint during the next pass.

## Better Uncertainty

At the beginning, the uncertainty was broad:

> We don't know whether account migration is feasible.

After working through the simulations, we could express the uncertainty more specifically:

> We can migrate accounts and preserve reporting consistency, but each plausible approach concentrates the risk in a different place.

That is real progress because now the uncertainty looks like regular old engineering work. Teams can now investigate whether the specific capabilities are technically achievable, compare alternatives, and eventually estimate the work.

You do not have to go back to leadership with a false promise of simplicity or a plea for more time for discovery. The answer is more concrete:

> We have three plausible ways to preserve historical reporting. One requires identity-preserving campaign imports, one requires rewriting historical events, and one introduces permanent identifier mapping across reporting. We need to validate the operational and technical risks of each before the estimate is meaningful.

That is a much more useful answer for the business than a rolled-up count of developer-weeks. Broad organizational uncertainty becomes a specific set of technical questions.

## Feasibility First

When I think back to the migration project now, the mistake was not just that we asked for estimates too early. It was that we never created a step where teams could bring their approaches together and see whether the parts formed a coherent system.

Estimates gave us an easy way to total up the work, but the numbers hid the architectural choices behind them. They didn't actually provide a direct answer to the question of whether we could build a good migration tool.

Feasibility work belongs before design, estimation, and work breakdown.

Bring the relevant people together and run each scenario far enough to see how the pieces fit, where the assumptions collide, and where the complexity moves. Pull in new participants as the scenarios expose constraints the group can't answer.

Only after we have vetted those plausible approaches together are we ready to choose one, decompose the work, and estimate it.
