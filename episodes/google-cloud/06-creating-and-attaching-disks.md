# Google Cloud #6 - Creating and attaching disks to VMs

By default when we create a new VM, we only have a boot disk where the operating system is installed.
But, more often than not, we need to store more data and this is usually done by adding an extra disk
onto our VM.

We can add upto 127 extra disks to a VM

## Types of new disk sources

We can create a new disk from two different types of sources

1. A blank disk that has nothing in it. We mostly use this
2. A new disk from a snapshot. We talked about snapshots in the previous lesson, we can create a new disk from it.


## Disk types in GCP

Source : [HERE](https://cloud.google.com/compute/docs/disks#disk-types)

When you configure a zonal or regional persistent disk, you can select one of the following disk types.

- Standard persistent disks (pd-standard) are backed by standard hard disk drives (HDD).
- Balanced persistent disks (pd-balanced) are backed by solid-state drives (SSD). They are an alternative to SSD persistent disks that balance performance and cost.
- SSD persistent disks (pd-ssd) are backed by solid-state drives (SSD).
- Extreme persistent disks (pd-extreme) are backed by solid-state drives (SSD). With consistently high performance for both random access workloads and bulk throughput, extreme persistent disks are designed for high-end database workloads. 


## Creating and attaching a disk

GCP doc on this is well made. Refer [THIS](https://cloud.google.com/compute/docs/disks/add-persistent-disk).

Once the disk is added, we need to format and mount it on the VM. The steps are explained in detail above.
But, here is the short form with only commands

```
# Find the newly added disk
sudo lsblk

# Example: Newly added disk is `sdb`
# Format it using mkfs. Make sure to replace sdb with correct disk

sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb

# Mount it. Example, we want it at /data
sudo mkdir /data
sudo mount -o discard,defaults /dev/sdb /data
```
At this point the disk is mounted, we just need to make sure that this gets mounted automatically whenever
the machine reboots.

This is done using adding an entry in **Fstab**

### Adding fstab entry

fstab : filesystem table

It's a simple configuration file located at `/etc/fstab` and is used to help us in mounting and unmounting
disks/devices onto our Linux system

```
# Make a backup in case we messup
sudo cp /etc/fstab /etc/fstab.backup

# Find the new disk's UUID
sudo blkid /dev/sdb

# Edit /etc/fstab using vim/nano etc and add
UUID=<UUID_VALUE> <mount point> ext4 discard,defaults,MOUNT_OPTION 0 2

# That is, in our case something like
UUID=UUID_VALUE /data ext4 discard,defaults,MOUNT_OPTION 0 2
```


