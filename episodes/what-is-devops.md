# What is DevOps

DevOps is a methodology in software development and release that aims to increase the speed
and efficiency at which software is released.

Before we even begin to talk about DevOps, we need to know what was there before DevOps.
What are the problems with the methods of the past


## Let's talk with a real example.

Let's say our company has a software as a service. Our software is something similar to Zoom, the video conferencing app.
Let's call it "Boom"

Boom has two components.

1. The server side service (Let's call it `Boom Server`)
2. The client application (like the zoom app on our laptop, let's call it `Boom Client`)


And there is only one team to manage the code for both

For the `Boom Server`, there is a Development environment (the Dev's laptop) and a production
environment. Same for the `Boom Client`

## The People involved

### Developers

They write code. These includes, but not limited to:
- Bug fixes (Ex: Boom crashes sometimes in certain operating systems)
- New features (Ex: We are adding a feature to help with noice cancellation during meetings)
- Security updates (Ex: There is a vulnerability that lets attackers compromise a computer running Boom)


Let's say there are only two environments. 


### Operations Team

They manage the servers where the `Boom Server` app is running.
- They make sure that the Boom servers are up and running
- They patch the server, update the OS, manage firewall etc
- They release new code given by the developers into the `Boom Server`
- They also make the latest `Boom Client` available to download

## Some potentially boring history

### Waterfall model - The old days

![Waterfall Model](img/waterfall-model.png)

- There are different phases in this model, each dependent on the output of the previous
- Once you are past a phase, you cannot go back, like a **waterfall**
- For example, you **cannot change** the design in the implementation stage
- This meant that there had to be precise planning and the requirements has to be perfect
- A good analogy is constructing a house. You cannot change the design once you're half way with building the roof, right?


Let's talk about our `Boom Video Calling App`, if we were do develop it following the waterfall
model, we would have to precisely know all the requirements before hand, make all the decisions,
write all the documentation even before the coding starts.
And, once the coding is started, there is no going back and changing the design.


#### The problems with waterfall model

Absolutely not flexible


### The other models following waterfall

Let's just say that there were a bunch of different models that tried to fix the issues with
the waterfall model. 
For example
- Rapid Application Development
- Dynamic Systems Development Method
- Extreme Programming
But let's not concern ourselves with these

### Agile

Read the agile manifesto [here](http://agilemanifesto.org/principles.html)

The TL;DR was that, the development process should be flexible such that "good" changes are 
always welcome. If the team came up with a really great idea, even towards the end of the "development", it was to be welcomed


- Individuals and interactions over processes and tools
- Working software over comprehensive documentation
- Customer collaboration over contract negotiation
- Responding to change over following a plan 

That is, according to Scott Ambler:

- Tools and processes are important, but it is more important to have competent people working together effectively.
- Good documentation is useful in helping people to understand how the software is built and how to use it, but the main point of development is to create software, not documentation.
- A contract is important but is no substitute for working closely with customers to discover what they need.
- A project plan is important, but it must not be too rigid to accommodate changes in technology or the environment, stakeholders' priorities, and people's understanding of the problem and its solution.


## How software was released

To keep things simple and in context, let's just take two scenarios. `Pre-DevOps` and `DevOps`

> Don't quote me on it, I am just trying to explain what "DevOps" is fixing


> For now, let's only talk about the `Boom Server App`. Imagine that there is a 
> `git` repository with the code and the `master` branch is the mainline
> And the developers work on their own branches when making a change

### Pre-DevOps 

1. The Developer wrote the app
2. They do some tests locally
3. The changes are **NOT** merged to the master until a certain point in time. They are usually large changes
4. The integration to the main branch is done on designated time (let's say we do it once a week)
5. The developer has to make sure that their changes do not have any conflict, fix any.
6. After a lot of mental gymanstics, the code is merged
7. Now we wait until the "deploy day"
8. The operations team has to make sure that the new code will work on production. They may need to update dependencies etc
9. Finally the deploy day comes and the operations team deploys it **manually**. By running some hacked together deploy script
10. If there are issues, the Operations team has to either rollback the change
11. The operations team has to make sure that the service is healthy, add more servers if needed etc


#### The problems with this

1. Integrating large changes once a while is more error prone. Imagine a scenario where the
developer `D1` started working on a feature if done fully adds 10,000 new lines of codes.
Meanwhile, developer `D2` is working on another bug fix that changed a lot of lines.
Towards the integration of both of these to the master, it is going to be such a pain in the neck
to make sure that the changes do not break things
2. The developer's environment is different from the production

![Works on my machine](img/works-on-my-machine.jpg)
