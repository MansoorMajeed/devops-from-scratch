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

##### b. UTS (UNIX Time-Sharing) namespaces 


##### c. IPC (InterProcess Communication) Namespaces


##### d. PID (Process ID) Namespaces


##### e. NET (Network) Namespaces


