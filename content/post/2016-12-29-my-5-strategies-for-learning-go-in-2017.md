---
title: My 5 Strategies for Learning Go in 2017
date: 2016-12-29 09:29:22 -0500
categories: 
- Code
- Golang
aliases: 
-  "/blog/2016/12/29/my-5-strategies-for-learning-go-in-2017/"
---
Over the past couple of years, one thing I've become more and more aware of is the unease and uncertainty of diving into a new project. Not matter what the new X is, I find I always go through the same set of uncomfortable feelings on my initial approach. 

Now, though, I'm starting to become familiar enough with this process that -- even though the discomfort doesn't go away in the initial learning stages -- I can embrace it, coexist with it, and forge ahead in learning, because of the strategies I'm going to lay out here.

<!--more-->
Heading into 2017, the new project I want to tackle is learning to write code in [Go](https://golang.org/). Here are the 5 strategies I've started using to reach that goal:

1. Attend live events, like the [Framingham Go Meetup](https://twitter.com/framinghamgo)
2. Read in-depth books, like [Go in Action](https://www.manning.com/books/go-in-action)
3. Do lots of coding exercises,  like [Go by Example](https://gobyexample.com/)
4. Make a mini project that puts these new concepts to use (coming soon)
5. Contribute to one of our live Go projects at work (The Big Goal)

It might seem like a scattershot approach, but having 5 different ways to come in contact with a new language has two layers of benefits: the things I learn directly in each context and the things that get woven together as a result of switching context between each approach.

Here are the "direct" and "crossover" benefits of each strategy:

## Attending Live Events

I wandered into my first [Framingham Go Meetup](https://twitter.com/framinghamgo) with almost no exposure to Go, which is what I did with Ruby a few years ago. A little intimidating? Yes. Did I feel out of place? Yup. Were people welcoming and friendly? Yes!

**Direct benefits:** Knowing full well that I would only understand bits and pieces of the talks at the first meetup, I still went for two reasons.

Now I have a benchmark for seeing progress -- in 6 months, maybe I'll think, "hey, I understood 70% of the talks this month!"

By meeting people and hearing about what they are working on and how they tackle problems with Go, I can start to think about applications and business logic I already understand through a Go lens.

**Crossover benefits:** Fully embracing the discomfort of being in a place where some part of you thinks you don't belong prepares you for taking on unknowns in every other mode of learning too.

**Bonus:** I got to hear directly from Bill Kennedy ([@goinggodotnet](http://twitter.com/goinggodotnet)), the author of Go in Action, which I had just started reading. Big Thanks for speaking to the group and sharing [these excellent resources](https://github.com/ardanlabs/gotraining/blob/master/reading/README.md).

## Reading Books

**Direct benefits:** Without previous experience in statically typed, compiled programming languages, there's a lot about Go that I just don't have exposure to. Having the background explained thoroughly in the long format of a book like [Go in Action](https://www.manning.com/books/go-in-action) is really helpful, even if I know I'm not going to retain everything on the first read.

As far as programming concepts go too, the explicit format of the book helps highlight places where I do know what's going on and I can draw comparisons to languages I already know.

**Crossover benefits:** In the last year, I've really recognized that if I'm actively reading a book on programming concepts, then I'm sharper every day when I go to code. I *think* this has to do with building better mental models about the work. As little as 10-15 minutes of theory reading a day helps me think more clearly about problems I'm trying to solve, even if they are unrelated to the book I'm reading.

## Coding Exercises

**Direct benefits:** While coding books do tend to have examples in them, I find a ton of added benefit to sites like [Go by Example](https://gobyexample.com/), where you can do exercise after exercise. I'm not necessarily talking about "coding challenges" either. Instead, I want to find examples that I can literally copy to reinforce the patterns and idioms used in Go. Rote learning here is tremendously helpful to get my fingers to start "thinking in Go."

**Crossover benefits:** After a while, I start jumping back and forth between books and exercises, to create stronger connections between the muscle memory in my hands and the concepts in my head.

For example, once I read the section on loops and conditionals, I thought, why not try Fizzbuzz:

```go
package main

import "fmt"

func main() {
	for i := 1; i <= 100; i++ {
		if i%15 == 0 {
			fmt.Println("fizzbuzz")
		} else if i%5 == 0 {
			fmt.Println("buzz")
		} else if i%3 == 0 {
			fmt.Println("fizz")
		} else {
			fmt.Println(i)
		}

	}
}
```
From past experience with simple code exercises in other languages, I know that I'll reimplement Fizzbuzz or something like it -- maybe with goroutines and channels?? -- a half dozen times over the next few months, as I pick up new concepts and styles.

## Mini Projects

I actually started out thinking this was the first thing I would do. Pretty soon, though, I realized that I'd rather get a foundation in the core concepts first and have some muscle memory, i.e. not have to look up the syntax for declaring variables or iterating over a slice.

**Direct benefits:** By pushing this project back a little bit, I can use it as a test of "the basics." Also, for what I have in mind (stay tuned!), I will need to dig into Go's standard library for things like making http requests and file IO. I'm considering these slightly more advanced explorations, once I feel comfortable with the flow of a simple program.

**Crossover benefits:** Hopefully, this stage will push me to ask some bigger design questions too and I'll have the chance to talk to my coworkers or people I've met from the meetups more about that.

## Production Code at Work

This is on my strategy list, but it's really a goal that will prove that I've done the work of all the other strategies.

**Direct benefits:** Not only would some production code be higher stakes than code I'd write in any of the other approaches -- nothing like production deployment pressure to accelerate learning! -- but I will also have the most context, because I've been writing code for the same platform, so I'll have lots of domain knowledge to guide me.

At Tapjoy, we've successfully ported portions of multiple Rails applications to Go services that run much more performantly. I have my eye on one particular area that I think could also benefit from a Go re-write. Aiming towards a working version of that application in Go in my spare time will be a great capstone for this entire learning process.

**Be sure to check back next December for "5 Improved Strategies for Really Learning Go, This Time, I Swear, in 2018".**