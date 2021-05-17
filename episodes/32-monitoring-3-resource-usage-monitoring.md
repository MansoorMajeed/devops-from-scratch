# VM Monitoring #3 - System Resource Monitoring Using Sensu

In the [monitoring introduction video](30-monitoring-1-infrastructure-monitoring-intro.md) we discussed about what are
the different types of resources we should be monitoring to keep an eye on the state of our systems.
These includes CPU, Memory, Disk usage etc.

In this one we will go ahead and actually implement these monitoring using Sensu

## Some sensu glossary

Before we get started with monitoring, we need to understand few terms sensu uses. Full list [HERE](https://docs.sensu.io/sensu-go/latest/learn/glossary/)

To keep things simple, I will only mention the terms that we will be needing now

### Agent

We know this one. It's a software that runs on the servers that we want to monitor. It sends keepalive, runs checks etc

### Check

A "check" the agent runs to determine the state of a system. For example, a "CPU" check to see the cpu usage.

Example:
```
type: CheckConfig
api_version: core/v2
metadata:
  name: check_cpu
  namespace: default
spec:
  command: check_cpu_usage.sh
  handlers:
  - email
  interval: 10
  publish: true
  subscriptions:
  - system
```

### Event

Represents the state of a server/service at any point in time. For example, if we had a check that looks for the CPU usage
and alerts if it above 90%, then when it goes above 90%, it is called an "event"

### Handler

Handler acts on events. For example, in the previous sample check, we had
```
handlers:
  - email
```
So, whenever an event occurs, we can handle it using handlers. Like sending an email, a slack message etc


### Assets

These are scripts/programs that helps us run checks. For example, we need a script that can run and look at the
CPU usage/ Disk usage etc. These executables are called assets.


## How does sensu monitors server resources

1. There are sensu "checks" which defines what sort of check it is. Refer example above
2. These checks makes use of "assets" or scripts to look at the resources and output "status code" based on what we need
3. For example: We can create a script that looks at the load average, and: 
    - if it is less than 80%, script exits with status code 0 (all good)
    - if it is above 80%, script exits with status code 1 (warning)
    - if it is above 90%, script exits with status code 2 (error)
4. The sensu "handler" upon seeing this, acts based on what we have configured it

## Let's go ahead and create resource monitoring

### 1. Adding the required dynamic assets

As mentioned in the previous block, we need some scripts to run and tell us what the state of the system is. We can either write
our own scripts for this. Something like
```
#!/bin/bash

LOAD=`uptime | awk '{print $8}' | cut -f 1 -d ,`

if [[ "$LOAD" > "2" ]]
then
  echo "ERROR: Cpu usage above 2"
  exit 2
elif [[ "$LOAD" > "1" ]]
then
  echo "WARN: Cpu usage above 1"
  exit 1
else
  echo "OK"
  exit 0
fi
```
But, we don't have to do that as sensu has a repository with all kinda scripts for most of our use cases.
And those scripts will be infinitely better than what we have 

For example, the [CPU checks plugin](https://bonsai.sensu.io/assets/sensu-plugins/sensu-plugins-cpu-checks) offers a ton of
features. So we will use this one instead

Let's register this dynamic runtime asset so we can use these scripts inside our agent
```
sensuctl asset add sensu-plugins/sensu-plugins-cpu-checks:4.1.0 -r cpu-checks-plugins
```
This example uses the -r (rename) flag to specify a shorter name for the dynamic runtime asset: cpu-checks-plugins

We also need the ruby runtime, because sensu-cpu-check is a ruby script that needs ruby to run
```
sensuctl asset add sensu/sensu-ruby-runtime:0.0.10 -r sensu-ruby-runtime
```

We can verify that these have been downloaded using
```
sensuctl asset list
```

### 2. Configure entity subscription

Every Sensu agent has a defined set of subscriptions that determine which checks the agent will execute. For an agent to execute a specific check, you must specify the same subscription in the agent configuration and the check definition

Let's call our subscription that has cpu check as "system", which makes sense since it is a system resource

We need to update our entity (our wordpress server) and include the "system" subscription

```
sensuctl entity list
sensuctl entity update <entity_name>
```

For Entity Class, press enter.
For Subscriptions, type system and press enter.

### 3. Creating the check

```
sensuctl check create check_cpu \
--command 'check-cpu.rb -w 75 -c 90' \
--interval 30 \
--subscriptions system \
--runtime-assets cpu-checks-plugins,sensu-ruby-runtime
```
This creates a check which will:
 - Use the `check-cpu.rb` script from the asset `cpu-checks-plugins` with warning 75% and critical at 90% CPU usage
 - The subscription is system
 - Runs every 30 seconds


Since we have created the check with subscription as `system`, if in any future if we create a new server and add it to
sensu with the subscription `system`, then that server will also automatically execute these checks.



### 4. Verifying

We can verify our brand new check
```
sensuctl check info check_cpu --format yaml
```

The Sensu agent uses websockets to communicate with the Sensu backend, sending event data as JSON messages. As your checks run, the Sensu agent captures check standard output (STDOUT) or standard error (STDERR). This data will be included in the JSON payload the agent sends to your Sensu backend as the event data.

It might take a few moments after you create the check for the check to be scheduled on the entity and the event to return to Sensu backend. Use sensuctl to view the event data and confirm that Sensu is monitoring CPU usage:

```
sensuctl event list
```
