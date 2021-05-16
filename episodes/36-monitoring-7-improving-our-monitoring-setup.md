# VM Monitoring #7 - Improving our monitoring setup

So far we have been creating everything by hand, editing the agents configs manually etc.
While this is the way for us to learn, it won't be a good idea to do the same in a production environment.

We should automate this.  I am not going to show you that, but will give pointers on how to do that so you
can try yourself

1. Each server we want to manage should have a it's agent.yml managed by configuration management tool such as ansible
2. When a new server comes online, this should get applied, and the server be registered with sensu-backend along with
predefined set of checks ready to go, without human intervention.
