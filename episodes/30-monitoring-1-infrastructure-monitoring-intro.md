# VM Monitoring #1 - Introduction to Infrastructure monitoring

We have multiple "servers" in our infrastructure. And we need to know if all of them
are doing well. We cannot check each of them manually to verify their health. This
is why we use monitoring tools.

## What to monitor

### 1. System resources

These are the basic resources only. As you advance and learn more, you will come across more and
more of these resources.

#### CPU

Each machines have a fixed number of CPU cores and they can be overloaded if we give them
more work than it can handle.

`Load Average` is one of the key metric we should know about

**Commands**
- `uptime` : shows uptime, load average
- `top` : Top processes
- `htop` : More user friendly tool to see running processes


#### Memory (RAM)

You know what this does. We don't want our machines to run out of memory and get our
important processes [OOM killed](https://www.kernel.org/doc/gorman/html/understand/understand016.html)

**Commands**
- `free` : Memory usage
- `free -h` : Memory usage in human readable form

#### Disk Usage

You know this one too. We need disk space to store files. We need to be alerted before
our system runs out of disk

**Commands**
- `df` : Shows disk usage
- `df -h` : Disk usage in human readable format

#### Disk IO Operations

That is, how busy our disk is. For example if there are a lot of disk intensive operations
going on (copying files, writing to the disk, reading from the disk etc) then our disk IO could
skyrocket and drag the entire system down.

**Commands**
- `iostat` : Shows IO information (Available in package sysstat)
- `iotop` : Top programs using IO

#### Network

How much data is being sent or received. A very high data rate could saturate the network links
and slow down the application's performance

### 2. Application health

Here, we want to make sure that our specific service running on the server is alive and well

#### Process running or not

This is one of the basic things we need to make sure. We want to be alerted if our service is down
(For example if our website is using Nginx, we want to know if it goes down)

**Commands**
- `ps` : Check for running processes
- `ps aux|grep nginx`  : See if nginx is running

#### Service responding correctly

Sometimes even if the process is running, it may be in a dead state where it does not respond to requests.
In case of a webserver for example, the correct way to know if it is working well is to actually make
an http request and see if it responds

**Commands**
- `curl`
- `curl -s localhost:8080` : Make an http request to localhost on port 8080 and see the response


### 3. Application Performance

Once we make sure our application is doing it's basic functions, the next important metrics to monitor
are the performance. We need to know if and when the application is performing poorly.

There are a ton of metrics to be monitored here depending on the application itself. For the sake of
simplicity we are only talking about two of them here

#### App response time

How fast does the application respond to requests. Each application will have a "usual" response time.
If it goes above this usual response time, it means something is wrong. It could be bad code, or the
servers behaving badly, network issue etc

#### Application error rate

Sometimes even when the application response time is good, it could be throwing a lot of errors (4xx or 5xx)
to the clients.

4xx means client side errors (Example : 404, 403, 401)
5xx means something wrong on the serve side (Example : 500, 502, 503)

Read about http status codes : [HERE](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
