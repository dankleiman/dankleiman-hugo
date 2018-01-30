+++
title = "Keeping an Engineering Notebook"
date = "2018-01-28T22:52:26-05:00"
categories = ['Code']

+++
The best upgrade I've made to my workflow in the past year was to start keeping an engineering notebook.

Whenever I start a new project, the first thing I do is create a new section in my engineering notebook. It's really simple. With a tiny script, I generate a dedicated folder for the new project, plus three sub-folders and a README:

```
    some_new_work
        |__ notes/
        |__ data/
        |__ scripts/
        |__ README.md
```

As simple as this structure seems, it has had a tremendous impact on my work. In this post, I want to try to unpack why and how I think that's working.

<!--more-->

## Less Scattered, More Focused

The first thing I've noticed is that focusing in on the new problem is easier when I know where I'm going to put all the files related to that project.

With sections for **notes**, **data**, and **scripts**, pretty much anything I touch has a natural home in a project subfolder. I tend to sketch out rough ideas about a particular part of the problem as a markdown file in the notes section. Then, as I develop some test code, I store it as a snippet in the scripts folder. If the script is a query or I have some backing data in an investigation, I can easily drop it into the data folder.

Not only does having a single folder per project help my workflow during the initial stages of a project, but I can easily come back to the projects months later and find artefacts that are still useful.

By accruing artefacts along the way to solving each problem, I can reproduce any part of the problem/solution and essentially "replay" my thinking at any point in time.

Having all the evidence in one places has also pushed me to be clearer about individual file names. Each file becomes a valuable piece of an audit trail of how I solved the problem.

## Rewriting and Deleting to Prune an Idea

Initially, I thought the main benefit was going to be that I would declutter my work space and have a somewhat more organized dumping ground for all my files and data.

But I discovered an even greater benefit by continuously organizing my files and folders: I gained more clarity about the problem every time I would rewrite, rename, or remove files from the notebook -- especially the README -- in a process I know think of as "pruning the idea."

Especially with thornier problems, I now see that I go through many stages of thinking that I understand the core issue and developing and testing hypothetical solutions. I use the README in this project set-up to keep track of the current state of hypotheses being proven or having been disproved.

Ultimately, I want the README to become a document I can share with my co-workers or other stakeholders in the project, so that's what I'm writing towards, polishing it a little at a time as I go.

In contrast, the documents in the `notes` section are either much more fragmented or are narrowly focused on one aspect of the project. The README pulls the best findings from the notes.

Over time, I shape the README into a high-level explanation of the problem, a narrative about the investigation, and the justification for a solution. For many issues, this ends up being a drop-in PR description for my code changes.

## Getting Set Up

The script I use to generate new project sections [lives here on github](https://github.com/dankleiman/notebook). As I said before, it's pretty simple. You spin up the same set of subfolders and a README each time.

When you run `notebook` there are two flags you can optionally pass:

```
-notepath string
    Main notebook directory set by env var NOTEPATH (default ".")
-section string
    Name for new section of this notebook (default "new_section")
```

By default, `notebook` will look for an environment variable called `NOTEPATH` that defines your main engineering notebook directory, but you can override this with the `notepath` flag.

Use the `section` flag to name the section you are creating in a meaningful way for the new project.

Run:

```
./notebook -section=new_project && cd $NOTEPATH/new_project && ls
```

And you will see your new section ready to be filled up with interesting data, scripts, and notes!
