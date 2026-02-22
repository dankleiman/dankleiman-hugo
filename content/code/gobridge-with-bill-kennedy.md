---
title: "GoBridge with Bill Kennedy"
date: 2017-02-12 15:18:04 -0500
categories: 
- Code
- Golang
aliases: 
-  "/blog/2017/02/12/gobridge-with-bill-kennedy/"
---

Last weekend, I had the chance to volunteer at a GoBridge event taught by Bill Kennedy of Ardan Labs. I'm trying to make [2017 my year of learning Go](/blog/2016/12/29/my-5-strategies-for-learning-go-in-2017/), so helping out at the event felt like a natural extension and a great way to connect with more people in the Go community.

Going in with Ruby as my first language, I braced myself for static typing and wanted concurrent programming to bend my brain, but that's not really what happened at all.

<!--more-->
Before we get into what I actually learned, I urge you to check out all of these related links if you want more background on the GoBridge, the instructor, and the training material:

- [GoBridge](https://golangbridge.org/) -- the inspiration for the event
- [Framingham Go](https://www.meetup.com/Framingham-Golang-Meetup/) -- the meetup group that organized the event
- [Ardan Labs Trainings](https://github.com/ardanlabs/gotraining#current-schedule) -- the instructor Bill Kennedy's company that teaches this and other events
- [Ultimate Go Training](https://github.com/ardanlabs/gotraining/tree/master/courses/ultimate) -- the source material, including design philosophy, practice exercises, and related reading, for the actual workshop

_Bonus: git clone the Go Training repo above into you $GOPATH, go build it, and it will run as a webserver you can launch locally, browsing all the coure material and links to code samples on the Go Playground._

And one more caveat: my Tai Chi teacher always talked about the challenges of teaching Tai Chi, which has to be experienced physically, to people who like to do abstract thinking. When someone tends to build a mental model for new information first, it's hard to get them to dive directly into the felt sensations, and as a result, they can come up with some pretty wacky ideas their first time through. He used to say it was like accidentally overhearing two young children describe what they thought sex was like. Of coure, the kids would have wildly inaccurate, innocent, and yet, elaborate ideas about it. And they would be hilariously far off from what the actual experience is like.

If I head into this post trying to tell you Go is X or Go does Y better than this or that language, I'm going to sound like those little kids. This is all new to me and I don't want to just parrot back something I've heard somewhere. I'll link out to better arguments when it comes to technical detail, but I do want to try to talk about what I continue to find interesting about learning Go.

## Design Software for Hardware

We started off the weekend with some [design guidelines](https://github.com/ardanlabs/gotraining/blob/master/reading/design_guidelines.md). Here's the first thing that really jumped out at me:

_"The most amazing achievement of the computer software industry is its continuing cancellation of the steady and staggering gains made by the computer hardware industry." - Henry Petroski_

Wait, so all that time I haven't been thinking about the relationship between the code I write and the hardware it runs on, I've actually been contributing to the "two steps back" phase of technological evolution???

We explored stack frames and memory allocation and passing values all with the notion that the performance characteristics of the underlying hardware should be factored into the way that your software is written and executed -- a concept with a fantastic name: **Mechanical Sympathy**. Here's where I take Bill's word for it and I won't try to make the case to you that Go is somehow the best way to achieve this hardware/software balance. But I will say that I am left feeling that the possibility of more powerful and efficient hardware/software unity is intriguing enough to pull me deeper into the story of Go.

**Homework:** Read everything in the [Mechanical Sympathy](https://github.com/ardanlabs/gotraining/blob/master/reading/README.md#mechanical-sympathy) section of the training repo.

## Shared Behavior over Shared State

Now, I'll let Bill introduce the other major hurdle I had to overcome with my object-oriented background. Starting around 5 minutes in the video, he explains a typical gotcha that people run into when they switch to Go from an object-oriented language. Even though the slides don't come out in the video, you'll be able to follow the issue.

<iframe width="560" height="315" src="https://www.youtube.com/embed/7YcLIbG1ekM?t=5m8s" frameborder="0" allowfullscreen></iframe>

Here is [code from the training repo](https://github.com/ardanlabs/gotraining/blob/master/topics/api/composition/grouping/example1/example1.go) that illustrates the problem. The comment at the top of the file sums up the problem: "This is an example of using type hierarchies with a OOP pattern. This is not something we want to do in Go. Go does not have the concept of sub-typing. All types are their own and the concepts of base and derived types do not exist in Go. This pattern does not provide a good design principle in a Go program."

```go

// All material is licensed under the Apache License Version 2.0, January 2004
// http://www.apache.org/licenses/LICENSE-2.0

// This is an example of using type hierarchies with a OOP pattern.
// This is not something we want to do in Go. Go does not have the
// concept of sub-typing. All types are their own and the concepts of
// base and derived types do not exist in Go. This pattern does not
// provide a good design principle in a Go program.
package main

import "fmt"

// Animal contains all the base fields for animals.
type Animal struct {
	Name     string
	IsMammal bool
}

// Speak provides generic behavior for all animals and
// how they speak.
// SMELL - This can't apply to all animals.
func (a Animal) Speak() {
	fmt.Println("UGH!",
		"My name is", a.Name,
		", it is", a.IsMammal,
		"I am a mammal")
}

// Dog contains everything an Animal is but specific
// attributes that only a Dog has.
type Dog struct {
	Animal
	PackFactor int
}

// Speak knows how to speak like a dog.
func (d Dog) Speak() {
	fmt.Println("Woof!",
		"My name is", d.Name,
		", it is", d.IsMammal,
		"I am a mammal with a pack factor of", d.PackFactor)
}

// Cat contains everything an Animal is but specific
// attributes that only a Cat has.
type Cat struct {
	Animal
	ClimbFactor int
}

// Speak knows how to speak like a cat.
func (c Cat) Speak() {
	fmt.Println("Meow!",
		"My name is", c.Name,
		", it is", c.IsMammal,
		"I am a mammal with a climb factor of", c.ClimbFactor)
}

func main() {

	// SMELL - I can't create a list of Cats and Dogs using
	// the Animal type. Can't create a list based on a
	// common set of state.

	// DOES NOT COMPILE

	// Create a list of Animals that know how to speak.
	animals := []Animal{

		// Create a Dog by initializing its Animal parts
		// and then its specific Dog attributes.
		Dog{
			Animal: Animal{
				Name:     "Fido",
				IsMammal: true,
			},
			PackFactor: 5,
		},

		// Create a Cat by initializing its Animal parts
		// and then its specific Cat attributes.
		Cat{
			Animal: Animal{
				Name:     "Milo",
				IsMammal: true,
			},
			ClimbFactor: 4,
		},
	}

	// Have the Animals speak.
	for _, animal := range animals {
		animal.Speak()
	}
}

// =============================================================================

// NOTES:

// Smells:
// 	* The Animal type is providing an abstraction layer of reusable state.
// 	* The program never needs to create or solely use a value of type Animal.
// 	* The implementation of the Speak method for the Animal type is a generalization.
// 	* The Speak method for the Animal type is never going to be called.

```

Reading the code above, especially for the notes, you can see that the OO mindset of grouping objects based on shared state, and then defining shared behavior for that heirarchy of objects, does not really hold up in Go. Instead, interfaces are defined by shared behavior -- or implementing the same set of methods. If a type implements all the methods defined by the interface, it _satisfies_ that interface.

So in our example above, instead of thinking about the shared parent class "Animal", Go pushes you to define an interface of "things that speak."

```go
	type Speaker interface {
		Speak()
	}
```

In order for a Dog or a Cat or Whatever other type to be a Speaker, it has to implement the Speak method. Sounds cool in theory, right? Here's the first practical example I came across that helped the concept click. 

In [Ben Johnson's Go Walkthrough series](https://medium.com/go-walkthrough), where he explores different packages in the Go standard library, he gives the example of the `io.MultiReader` function. The `Reader` interface, like our `Speaker` interface above, is satisfied when a type can read a stream of bytes.

In the MultiReader example, Ben asks, "what if you are trying to send a POST request and you want to combine the header data you have in memory, with the contents of a file you have on disk?" Since you can access the in-memory data and file contents via `Read` functions, the info you need can be passed into `io.MultiReader` which accepts multiple input readers and concatenates them.

So in OO land I wouldn't group a file and header data as the same class of object, but if you drill into their behavior given the particular functionality we need, then you can easily see what they have in common.

At first, seeing this difference in grouping by behavior over state was a little overwhelming - "oh gosh, I'm going to have to rethink all the heirarchies and abstracts I need to make as I'm planning out my code." But again, Bill was very reassuring here. Here was the essence of it:

<iframe width="560" height="315" src="https://www.youtube.com/embed/mDYCLFE86Po" frameborder="0" allowfullscreen></iframe>

And if you want to see how you solve one problem at a time in your code, go back to the first video in this post for a very elegant example.

## For Further Training

Check out the full list of [Ardan Labs courses](https://github.com/ardanlabs/gotraining/tree/master/courses) along with other recommended Go training materials like [Exercism.io](http://exercism.io/languages/go/about).