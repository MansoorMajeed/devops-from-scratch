# Our Goal

To learn what Kubernetes is while trying to solve a real world problem

## The problem

So, we have a simple application written in Golang, we want to run multiple copies of it
on a server.

For this demo, we will use [THIS go-hello-world](https://github.com/MansoorMajeed/go-hello-world) demo app.
So, we want to run this app with multiple copies and be easily scalable. This way, if we have more traffic, we
can easily increase the number of copies of our app (manually first and automatically afterwards).
Additionally, this provides a fault tolerance so that even if one copy of our app goes down, it does not affect the users