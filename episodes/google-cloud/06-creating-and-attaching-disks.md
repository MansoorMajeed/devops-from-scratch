# Google Cloud #6 - Creating and attaching disks to VMs

By default when we create a new VM, we only have a boot disk where the operating system is installed.
But, more often than not, we need to store more data and this is usually done by adding an extra disk
onto our VM.

We can add upto 127 extra disks to a VM

## Types of new disks

We can create a new disk from two different types
1. A blank disk that has nothing in it. We mostly use this
2. A new disk from a snapshot