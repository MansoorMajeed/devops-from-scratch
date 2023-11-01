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

Isolates two system identifiers: the hostname and the NIS domain name.
This allows each container to have its own hostname.

##### c. IPC (InterProcess Communication) Namespaces

IPC namespaces in Linux isolate inter-process communication mechanisms, ensuring 
processes in different namespaces cannot directly communicate using shared memory, 
semaphores, or message queues. 
This is especially valuable in containerized environments to prevent interference 
between instances. 

Essentially, it's like giving each container its own private communication channel.

##### d. PID (Process ID) Namespaces

Isolates the process ID number space. This means that processes in different PID 
namespaces can have the same PID. For instance, multiple containers can each have 
its own "PID 1".

##### e. NET (Network) Namespaces

Isolates network devices, IP addresses, IP routing tables, port numbers, etc. 
A process in one NET namespace can't see or directly communicate with network 
devices or local network resources of another namespace.

#### 2. Control Groups (Cgroups)

Cgroups control how much CPU, memory, network bandwidth, and disk I/O can be used by the processes within a container. This ensures that a single container cannot starve others of resources.

Example: If you have a database and a web server running in separate containers on the same host, you can allocate more memory to the database and limit the CPU usage of the web server to ensure balanced performance.


#### 3. Union File Systems

UnionFS allows layers in container images. Multiple containers can share the same base image layer, while each has its own unique layer for customized files and changes. This saves space and aids in fast container spin-up times.

#### 4. Capabilities

Capabilities in Linux split the privileges traditionally associated with root into distinct units, allowing finer-grained control over permissions. Instead of granting a process all-or-nothing "root" access, specific capabilities like network administration or file ownership changes can be assigned individually. This approach enhances security by limiting the potential impact of privilege escalation. In essence, capabilities allow a more nuanced delegation of power and responsibilities to processes on a Linux system.
