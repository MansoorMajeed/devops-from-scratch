# Google Cloud #3 - Instance Templates, Static IP Addresses

## Instance Templates

When we create a new VM from the dashboard, we have to select a lot of options. If we create many VMs,
then this can get tedious and repetitive. Solution is to use instance templates

Instance templates allow us to create a template that already specifies characteristics of our VMs
like the instance type, disk, firewall rules etc. This way we can easily create a new VM from a template
without having to worry about setting the specs

## External IP Addresses in GCP

In GCP there are two differen types of IP addresses
1. Ephemeral
2. Static

### Ephemeral addresses

Ephemeral means short lived

By default each VM we create have an ephemeral address. This IP address will not change while the VM is running.
But it **could** change if we stop the VM and later start it back

Why ephemeral? Because it is cheaper

### Static addresses

We can get a static IP from a pool of IP addresses GCP owns and then we can assign it to any instance.
This IP will not change unless we release it from the pool

### When to use static addresses?

If we are going to use a VM for anything semi permanent and if we would like the IP to not change, then we should
create a static IP address and use it. For example, if we have a website hosted in the VM, then we may need to use static
address.

Ephemeral addresses are fine for instances that are behind a load balancer (more on this later)