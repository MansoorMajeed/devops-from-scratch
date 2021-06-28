# Google Cloud #4 - Virtual Private Cloud (VPC) Networks

We know what a "network" is. It is when  we connect computers together wired or wirelessly.
For example, our home wifi network, or a bunch of servers connected using a switch and ethernet cables.

A VPC network is similiar, but instead of being physical networks, they are logical. So, a VPC is a virtual network created
inside of Google's infrastructure using Andromeda. Andromeda is a software defined network. We are not gonna discuss about it
now.

Google VPCs are Global. Meaning we can have two machines in different region to be in the same VPC network

## Why use a VPC

By default when we create a GCP project, a `default` network is created. So we are already using a VPC network.
So, by default all the new VMs we create are part of this `default` network.

Checkout this diagram by GCP : [HERE](https://cloud.google.com/vpc/images/vpc-overview-example.svg)

Even then, why do we need a network? 

Let's say we have a VPC network called `production` and this contains all the VMs that is powering our production infrastructure.


1. All the VMs can talk to each other through this private network, without going through the internet
2. We can restrict VMs internet access, like maybe a few servers don't need internet access at all.
3. Since this is a private network, the bandwidth costs are saved a lot
4. Performance is also a lot better than going through the internet
5. We have a great control over what machine can connect to what using firewalls
6. We can use internal load balancers.

## Firewall Rules

By default in a new network, nothing can connect to each other. We need firewall rules to make that happen.


### Network tag

In GCP we can add a network tag to each instance. Using this we can create firewall rules. 

![VPC Network](img/vpc-nw-example.jpg)

Consider this setup. If we add tag `nginx-proxy` to Nginx, `webapp` to the web app 1 and 2, and `database` to the database
server.

Now we can create firewall rules saying

1. allow `nginx-proxy` to talk to `webapp` on port `80` over protocol `tcp`
2. allow `webapp` to talk to `database` on port `3306` over protocol `tcp`

> We can use source and target tags for firewall rules, but this is only applicable for internal traffic
> It does not work for external traffic

