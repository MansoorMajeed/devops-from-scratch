# Google Cloud #7 - Setting up Gcloud CLI

So far we have been doing everything in GCP through the UI, while it is great and userfriendly, there are much more
efficient way of doing things in GCP. One such way is the `gcloud` command line utility

## What is gcloud

[Gcloud](https://cloud.google.com/sdk/gcloud) is a command line tool by Google that lets us manage most of the GCP
products from the terminal.

### What can it do?

Pretty much anything we use the UI for.

- Create/manage/edit instances, firewall rules, load balancers, permissions etc

### But why use it?

Because sometimes it is much faster to use the CLI than to go through the UI and click buttons. Also, we can use the 
utility to automate managing resources

Example:

Let's say you want to create 10 instances with some slightly different parameters like disk space/cpu cores etc,
using the UI to do that 10 times would be very inefficient as it can take a lot of time and it is error prone too.

But, using the CLI, we can do that easily. 

We can create custom scripts to get our job done really quickly. 

The more you use it, the more you will come to love it.

## Installing gcloud

`gcloud` is part of the Google Cloud SDK. So, we need to install that first. This is a very straight forward thing to do.

Just go [HERE](https://cloud.google.com/sdk/docs/install) and follow the instructions for your operating system.

