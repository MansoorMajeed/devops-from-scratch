# VM Monitoring #7 - Sensu Go in Production considerations and closing thoughts

## Deployment Architecture

Find more details [HERE](https://docs.sensu.io/sensu-go/latest/operations/deploy-sensu/deployment-architecture/)

In the past few videos when we talked about sensu, we were using a single instance sensu setup. That was good enough
for us to learn the basics of sensu and get a conceptual idea of how everything works together. But in a production environment,
we need fail over, better security etc

In this video/notes, I will be discussing what all to consider when you move your sensu deployment to production

## Clustered deployments

Having a single host is not a good idea in a production environment.  

## Using with configuration management

So far we have been creating everything by hand, editing the agents configs manually etc.
While this is the way for us to learn, it won't be a good idea to do the same in a production environment.

We should automate this.  I am not going to show you that, but will give pointers on how to do that so you
can try yourself

1. Each server we want to manage should have a it's agent.yml managed by configuration management tool such as ansible
2. When a new server comes online, this should get applied, and the server be registered with sensu-backend along with
predefined set of checks ready to go, without human intervention.

## TLS for etcd

Reconfiguring a Sensu cluster for TLS post-deployment will require resetting all etcd cluster members, resulting in the loss of all data. So, when you are creating a production sensu setup, keep this in mind. You may want to enable TLS in the beginning itself

## TLS for Sensu UI and API

We did not use any kind of TLS in our sensu setup. But when it comes to a production setup, we definitely need TLS.
You should use something like an Nginx proxy in front of the sensu UI and configure TLS in the Nginx server so that
the sensu UI, API etc are behind TLS. You should not be sending credentials over plain text

