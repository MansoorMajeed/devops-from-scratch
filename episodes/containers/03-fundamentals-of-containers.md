# Fundamentals of Linux Containers

## Linux Container Architecture

Most of the components required by the containers in Linux are provided by the Linux
Kernel itself. 

### What do we need from containers?

Before we talk about the architecture of Linux containers, it is important that we 
have an understanding of what we NEED from a Linux container. This will help us 
understand each component better

#### 1. We need application isolation

That is, when we "containerize" an application (a process), it should be truly contained.
That way, another process should not be able to interfere with it. This would mean
isolation on process level, network level, file system level etc. 


#### 2. We should be able to allocate and limit resource to containers

We should be able to tell that this container gets this much CPU, Memory, network bandwidth etc.
This is to ensure that a single bad container cannot starve other containers of resources.


#### 3. Be able to share common files efficiently

Allow containers to be lightweight and share common files efficiently.

#### 4. Enhance security by reducing privileges

Each process should have the minimum privileges it requires to run its functions.

### How do we achieve those needs?

So we talked about what are the needs as listed above, now we will discuss how we 
achieve each of those needs

We will also use some practical examples to show how it looks in real world.
You don't really need to know each of these commands, this is just to reinforce
the concepts

We will create two containers to show the examples. `container1` and `container2`

```bash
# Start two containers in detached mode
docker run -d --name container1 busybox sleep 3600
docker run -d --name container2 busybox sleep 3600
```

Now let's run them in the background, we will get to them below.

#### 1. Namespaces

Read more about namespaces [HERE](https://man7.org/linux/man-pages/man7/namespaces.7.html)

Namespaces are a way to achieve this isolation we talked about. There are different
types of namespaces that achieves these different goals such as process, network isolation

       A namespace wraps a global system resource in an abstraction that
       makes it appear to the processes within the namespace that they
       have their own isolated instance of the global resource.  Changes
       to the global resource are visible to other processes that are
       members of the namespace, but are invisible to other processes.
       One use of namespaces is to implement containers.

##### a. MNT (Mount) Namespaces

Isolates the set of filesystem mount points seen by a group of processes.
Processes in different MNT namespaces can have different views of the filesystem hierarchy.


Example:
So we create a file in container1
```
docker exec container1 touch /container1_file.txt
```
Which we can see in `container1`

```
➜  ~ docker exec container1 ls -lh /container1_file.txt
-rw-r--r--    1 root     root           0 Nov  1 17:49 /container1_file.txt
➜  ~
```

But that does not exist in `container2`
```
➜  ~ docker exec container2 ls -lh /container1_file.txt
ls: /container1_file.txt: No such file or directory
```

##### b. UTS (UNIX Time-Sharing) namespaces 

Isolates two system identifiers: the hostname and the NIS domain name.
This allows each container to have its own hostname.

```
➜  ~ docker exec container2 hostname
8e2992d0bcb0


➜  ~ docker exec container1 hostname
7c49e6148e5f
```

##### c. IPC (InterProcess Communication) Namespaces

IPC namespaces in Linux isolate inter-process communication mechanisms, ensuring 
processes in different namespaces cannot directly communicate using shared memory, 
semaphores, or message queues. 
This is especially valuable in containerized environments to prevent interference 
between instances. 

Essentially, it's like giving each container its own private communication channel.

Example:
Create two containers with distinct IPC namespaces:

```
docker run -d --name ipc_container1 --ipc private debian sleep 3600
docker run -d --name ipc_container2 --ipc private debian sleep 3600
```

Create a shared memory segment in ipc_container1:
```
docker exec ipc_container1 sh -c "ipcmk -M 1M"
Shared memory id: 0
```
This command creates a shared memory segment of size 1MB. You'll get an ID (let's say 0) as an output.

Try to access the shared memory segment from ipc_container2:
```
docker exec ipc_container2 ipcs -m

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status
```
This command lists shared memory segments. You'll observe that the memory segment created in ipc_container1 is not visible in ipc_container2.

But it looks like this from the same container
```
➜  ~ docker exec ipc_container1 ipcs -m

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status
0xced66e11 0          root       644        1048576    0
```



##### d. PID (Process ID) Namespaces

Isolates the process ID number space. This means that processes in different PID 
namespaces can have the same PID. For instance, multiple containers can each have 
its own "PID 1".

```
➜  ~ docker exec container1 ps

PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
   37 root      0:00 ps


➜  ~ docker exec container2 ps

PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
   19 root      0:00 ps
➜  ~
```

Here we can see that both the containers have a process with ID 1

##### e. NET (Network) Namespaces

Isolates network devices, IP addresses, IP routing tables, port numbers, etc. 
A process in one NET namespace can't see or directly communicate with network 
devices or local network resources of another namespace.

Let us see this in action
```
➜  ~ docker inspect container1 -f '{{.NetworkSettings.IPAddress}}'
172.17.0.2

➜  ~ docker inspect container2 -f '{{.NetworkSettings.IPAddress}}'
172.17.0.3
```
Here we can see that both the containers have their own unique IP addresses.

#### 2. Control Groups (Cgroups)

Cgroups control how much CPU, memory, network bandwidth, and disk I/O can be used by the processes within a container. This ensures that a single container cannot starve others of resources.

To show a real world example, let us run a container with a 50% of a core cpu limit.
```
docker run -d --name cpu_limited_container --cpus="0.5" busybox sleep 3600
```

And now let us mimick a high CPU usage on that container
This is an inifinite loop that will usually cause a 100% CPU usage.
```
docker exec -it cpu_limited_container sh -c "while true; do :; done"
```

But let's see how much CPU it is actually using

![CPU Usage](./diagrams/cpu-usage-container.png)

As we can see that the cpu usage is only 50%. This is especially important when we are running multiple
containers on the same host. Otherwise, a faulty process can starve the entire host of CPU or memory and
will cause issues on all the other containers. You would be surprised at how often this happens in real world
because developers forgets to put a limit on containers

#### 3. Union File Systems

UnionFS allows layers in container images. Multiple containers can share the same base image layer, while each has its own unique layer for customized files and changes. This saves space and aids in fast container spin-up times.

Let us go through an example to see this in action:

a. Start a container from a base image, and from inside the container, we create a file.
```
docker run -it --name ufs_container debian bash


root@ba4163deed36:/# echo "Hello from container!" > /hello.txt
root@ba4163deed36:/#
root@ba4163deed36:/# exit
exit
```
b. Commit the changes to a new image
```
➜  ~ docker commit ufs_container new_image_with_hello

sha256:6085f1c95cd9410cc648dfc26f0a50c0cbb26ededaff6bdf380f71d583963a06
➜  ~ docker images | grep new_image
new_image_with_hello      latest     6085f1c95cd9   11 seconds ago   139MB
➜  ~
```

c. Start a new container with the original image
```
docker run -it debian bash

root@a036aa58b40e:/# ls -l /hello.txt
ls: cannot access '/hello.txt': No such file or directory
root@a036aa58b40e:/#
```
As you can see, the file does not exist there (in our original image)

But if we start a new container with our new image, 
```
➜  ~ docker run -it new_image_with_hello bash

root@38b2cd3724b1:/# ls -l /hello.txt
-rw-r--r-- 1 root root 22 Nov  1 18:27 /hello.txt
root@38b2cd3724b1:/#
root@38b2cd3724b1:/#
```
You can see that our file exist there.

Now if we look at our new image using the following command
```
➜  ~ docker inspect new_image_with_hello | jq '.[0].GraphDriver.Data'

{
  "LowerDir": "/var/lib/docker/overlay2/b021905b310da2de7b9f3d8a206615e252cea0f17cdd66ead5b8003e9eb2d04a/diff",
  "MergedDir": "/var/lib/docker/overlay2/59305b5da031f2f4ae09a30ab6d0ab7d897b53329cf3aca34bc34899bdb0a887/merged",
  "UpperDir": "/var/lib/docker/overlay2/59305b5da031f2f4ae09a30ab6d0ab7d897b53329cf3aca34bc34899bdb0a887/diff",
  "WorkDir": "/var/lib/docker/overlay2/59305b5da031f2f4ae09a30ab6d0ab7d897b53329cf3aca34bc34899bdb0a887/work"
}
```

each change in a container creates a new layer, and layers can be stacked in a union to present a single coherent file system. Shared layers between containers make them efficient in terms of storage, as they can reuse these layers, and any modifications result in new, separate layers without affecting the shared ones.

#### 4. Capabilities

Capabilities in Linux split the privileges traditionally associated with root into distinct units, allowing finer-grained control over permissions. Instead of granting a process all-or-nothing "root" access, specific capabilities like network administration or file ownership changes can be assigned individually. This approach enhances security by limiting the potential impact of privilege escalation. In essence, capabilities allow a more nuanced delegation of power and responsibilities to processes on a Linux system.


Example:

Let us run a container that have no `CHOWN` capability, which means the container won't
be able to run `chown` command.
```
docker run -d --name container_no_chown --cap-drop CHOWN busybox sleep 3600
```
Let's see what happens when we try to run a `chown` within the container

```
➜  ~ docker exec container_no_chown chown 1000:1000 /tmp
chown: /tmp: Operation not permitted
```

If we were to run the same command on a container that does not have this capability removed,
like our `container1`, this will not produce an error and instead will change the ownership of
the directory

```
➜  ~ docker exec container1 chown 1000:1000 /tmp
➜  ~
```
