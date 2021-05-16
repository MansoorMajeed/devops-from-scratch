# VM Monitoring #2 - Getting started with VM monitoring using Sensu

In the previous video we discussed about what monitoring is and what all need to be
monitored. In this one we will be setting up monitoring using Sensu.

> Bear in mind that all these are talking about monitoring virtual machines. We have not reached
containers yet and hence we are leaving them out of the picture

## What is sensu?

Sensu is tool that will help us in monitoring our servers. Let's keep it simple.

We will obviously see what it can do real soon


This doc is mostly sourced from Sensu official documentation [HERE](https://docs.sensu.io/sensu-go/latest/operations/deploy-sensu/install-sensu/)


## Sensu Architecture

### Sensu Agent

This is a lightweight software that runs on each server that we want to monitor.
These agents sends information about the status of each server it is running, back to the
sensu backend server

### Sensu backend

This is where the magic happens. The sensu backend can send checks to each client, 
look at the status etc. 


## Setting up Sensu Backend

### Install sensu backend

We will be using our Debian 10 virtual machine as usual

```
# Add the Sensu repository
curl -s https://packagecloud.io/install/repositories/sensu/stable/script.deb.sh | sudo bash

# Install the sensu-go-backend package
sudo apt-get install sensu-go-backend
```

### Configure and start sensu backend

```
sudo curl -L https://docs.sensu.io/sensu-go/latest/files/backend.yml -o /etc/sensu/backend.yml

sudo systemctl start sensu-backend
sudo systemctl status sensu-backend
```


To begin with, this is the only config option that is enabled

```
state-dir: "/var/lib/sensu/sensu-backend"
```

### Initialize sensu backend.

We need to setup our admin username and password

```
export SENSU_BACKEND_CLUSTER_ADMIN_USERNAME=<username>
export SENSU_BACKEND_CLUSTER_ADMIN_PASSWORD=<password>
/usr/sbin/sensu-backend init
```


### Login to the admin panel

Login to 192.168.33.30:3000 or whatever is the IP address of the VM with the usernamd
and password from above

Let's also verify that the API is working fine

```
curl http://ip:8080/health
```


## On the workstation

Now that we have sensu backend running, let's install `sensuctl` on the local workstation.
Sensuctl is a cli tool used to manage Sensu

To install it on Linux machine:

```
# Add the Sensu repository
curl -s https://packagecloud.io/install/repositories/sensu/stable/script.deb.sh | sudo bash

# Install the sensu-go-cli package
sudo apt-get install sensu-go-cli
```
Follow instructions [HERE](https://docs.sensu.io/sensu-go/latest/operations/deploy-sensu/install-sensu/#install-sensuctl) to install
sensuctl for other operating systems (your local machine)


To start using sensuctl, we need to configure it with the username, password and the
address to reach our sensu backend api


From your local machine (not the sensu-backend server)
```
sensuctl configure -n \
--username 'admin' \
--password 'password' \
--namespace default \
--url 'http://192.168.33.30:8080'
```

Run `sensuctl config view` and it should show something like

```
❯ sensuctl config view
=== Active Configuration
API URL:                  http://192.168.33.30:8080
Namespace:                default
Format:                   tabular
Timeout:                  15s
Username:                 admin
JWT Expiration Timestamp: 1620564854
```

That means sensuctl is all good to go. With these steps, sensuctl has written the authentication details into 
```
~/.config/sensu/sensuctl/profile

and

~/.config/sensu/sensuctl/cluster
```


## Setting up sensu agents

Now that we have sensu-backend is up and running, we are ready to monitor our servers.
We need to install `sensu-agent` on the servers we want to monitor


### Installing sensu agent
For our use case, I am gonna install sensu-agent on our wordpress server.

```
# Add the Sensu repository
curl -s https://packagecloud.io/install/repositories/sensu/stable/script.deb.sh | sudo bash

# Install the sensu-go-agent package
sudo apt-get install sensu-go-agent
```

### configuring sensu agent

For each agent, we need a config file `/etc/sensu/agent.yml`. The bare minimum requirement is the `--backend-url`, because obviously the agent needs to know where to connect to.

> On the Vm we want to monitor:

```
# Copy the config template from the docs
sudo curl -L https://docs.sensu.io/sensu-go/latest/files/agent.yml -o /etc/sensu/agent.yml
```

In the config file, uncomment the below
```
#backend-url:
#  - "ws://127.0.0.1:8081"
```
and change it to the sensu-backend IP address. And
```
# Start sensu-agent using a service manager
service sensu-agent start
```

By now, the agent should have automatically configured itself and is talking to the sensu-backend. 

Sensu keepalives are the heartbeat mechanism used to ensure that all registered agents are operating and can reach the Sensu backend. To confirm that the agent is registered with Sensu and is sending keepalive events, open the entity page in the Sensu web UI or run `sensuctl entity list`

## Verify an example event

```
curl -X POST \
-H 'Content-Type: application/json' \
-d '{
  "check": {
    "metadata": {
      "name": "check-mysql-status"
    },
    "status": 1,
    "output": "could not connect to mysql"
  }
}' \
http://localhost:3031/events
```