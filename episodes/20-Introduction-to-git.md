# Introduction to Git

Video Link [HERE](https://www.youtube.com/watch?v=uxE2Le64vHk&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=21)


## What is the Problem we are solving?
If you are working on a project,
- You need to have some sort of way to keep track of all the changes that is happening in your project.
- You need to be able to see what changed, when, by whom
- You need to be able to see the difference in the files you just worked on and compare it with how it was in a point in time
- You need to be able to revert a mistake you made
- Multiple people should be able to work on the same code base withou messing up everything etc

Solution? **Version Control Software**

## What is Git

Git is an open source version control software, used to, well, version control
Version control simply means keeping track of changes to your projects as it grows

## Installing Git

- You can install git on windows on WSL or install Git Bash
- On MacOS, you can do `brew install git`
- On any Linux distro `sudo apt-get install git` or `sudo dnf install git` or `sudo yum install git` should work

## Git vs GitHub

- Git is the open source tool  
- Github is an online web based "git" hosting service

## Personal Advices

- Don't use GUI tools to learn git, just don't. Use the command line
- Don't try to cram everything at once. Learn the basics, use them regularly
  and use Google when you get stuck
- If you mess up your repository, instead of trying to clone a fresh copy of the
  repository, try to fix it. That is how you learn

## Git Repositories

A repository simply means a place to store your project and the changes to it

There are two types of repositories **Local** and **Remote**

### Local Repository

Means it sits on your computer's hard drive (or SSD, you know). 

### Remote Repository

Sits on another computer. Git can work over HTTP or SSH. More on it later
If you have multiple people working on the project, you probably need a remote
repository
Also, if you want to have a copy of your project somewhere other than your
computer, you need a remote repository

# Let's Git Started

This will be quick

## Configure your name and email

Before you start, let's first configure your name and email so that git knows
who is making the changes. More on it later

```shell
git config --global user.name "Mansoor"
git config --global user.email "m@esc.sh"
```

## Very Basics 

- `git init` - Initializes a local repository
Means, the current directory is under git now. 

Look at `ls -la .git` and you can see where the git magic happens

- `git status` - Shows the current status of the repo

### Staging changes - `git add`

**Create a new file** and use `git add <filename>` to add it to **staging area**


- `git add .` - add the current directory
- `git add directory/another` - Add a specific directory to staging
- `git add *.py` - add all .py files
- `git add f*` - Add everything starting with `f`.

You get the idea

### Commiting changes - `git commit`

**Commiting** means to commit to the change you just made. Meaning git will store
this change in it's magic storage (`.git` directory)

- `git commit` - Opens the editor (set by the $EDITOR environment variable - You can change it
using `export EDITOR=editor_name`) where you can write a commit message

**Commit message** is what will be recorded as a message identifier for your change

- `git commit -v` - Does the same thing as above, but shows the changes too, in the editor

- `git commit -m "A beatuful short description of the changes"` - Commits instantly with that message


> Why do we need staging area?
> Because you may not want to store all the files in git. Like temporary
> files, log files etc

### Ignoreing certain files

You can use the `.gitignore` file to do that. Just create a file of the name
in the git repository and add what you want to be ignored

Example:

```
foobar
cache/
```

This will ignore `foobar` and `cache` from being stored in git 

### Viewing the history of changes - `git log`

- `git log` - View all the commits in the current repository
- `git log -p` - View all the commits and the changes
- `git log -p <filename/folder>` - Show changes, but for the file/folder


### Viewing what change you just made - `git diff`

After you made a change to a file, before commiting, if you want to see what change you just did

`git diff` - Show the diff since last commit


## Branches

Git allows multiple people to work on the same repository without messing
up everything. This is achieved using branches

`master` is the default branch. It should be respected and try not to mess it up

If you want to work on two independent changes to your code base, branches are your
friend

Example: `fix-bug` branch to fix an emergency bug, and `feature1` to parallely work on a 
feature

> Branches do not know of the changes in each other until you merge them

- `git branch` - Shows the current branch
- `git checkout <branchname>` - Switches to branchname
- `git checkout -b <branchname>` - Create a new branch "branchname" and switches to it

> Note: When working on a new feature, we usually do `git checkout -b featurename` from 
> the `master` branch

### Merging the changes

Once you are done with all the changes in your `feature` branch, You can merge it to master
using `git merge feature` while on the master branch


While on `feature` branch, `git merge master` will merge the master branch onto your `feature` branch
This is usually needed to keep your `feature` branch up to date with the master branch



