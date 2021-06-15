# Google Cloud #2 - Hosting a simple website on Google Compute Engine - Our first VM

## Foreword

There are a lot of Google Cloud products and it would be confusing to just get started with them
directly. Instead what I would like to do is take one use case and find a product that will fit our requirement.

In the past videos we have been doing this, like, we want to host a website. How can we do that.

So, we will do the same here

## Our Goal

Host a simple website `simple.demo.devopsfromscratch.com` in Google Cloud Platform (GCP)

## GCP Product we will use - Google Compute Engine (GCE)

GCE is the offering of GCP where we can launch virtual machines in Google's infrastructure.
It is equivalent to EC2 in AWS

## Steps

1. Get GCP free trial account
2. Launch VM
3. Access the VM over ssh, install nginx
4. Point DNS, demo


## Key Concepts relating to GCE

### Region

Which region on earth the datacenter is located : Example `us-east4`

### Zones

Each region will have multiple datacenters in different zones. Example `us-east4-a, us-east1-b, us-east1-c`
Equivalent to availability zones in AWS

### Machine Family

Read more about [HERE](https://cloud.google.com/compute/docs/machine-types)

These basically means the kind of physical machines that are running these VMs. 
 - General purpose : For people like us with no need for high performance/memory
 - Compute-optimized : If you want to run really compute heavy applications
 - Memory-optimized : If you want VMs with terrabytes of RAM
 - GPU : If you want a GPU attached to your VM so you can do GPU intensive stuff

### Series

What kind of CPU these machines have. We usually want to go with the newest and cheapest option
For our use cases E2 is plenty enough

### Machine type

What size our VMs should be. This entirely depends on what we want to do with our VM
For small websites, blogs, development purposes etc `e2-micro -> e2-medium` should be good enough

#### Shared core

In this, our VMs are not really getting a full CPU assigned. Instead it is divided with other VMs.
the advantage is that it is considerably cheaper. And most of the time, the performance is good enough for our use

e2-micro sustains 2 vCPUs, each for 12.5% of CPU time, totaling 25% vCPU time.
e2-small sustains 2 vCPUs, each at 25% of CPU time, totaling 50% of vCPU time.
e2-medium sustains 2 vCPUs, each at 50% of CPU time, totaling 100% vCPU time.

### Firewall

The network firewall configuration allows us to allow/deny network access to our VMs/services
More about this in the next video

### Boot disk

Here we can choose which operating system we would like to have and the size of our main/boot disk.
