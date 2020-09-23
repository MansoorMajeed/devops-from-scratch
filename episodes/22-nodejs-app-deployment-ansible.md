# Deploying a simple NodeJS based app with Nginx Load balancer


Video Link [HERE](https://www.youtube.com/watch?v=HCbc-m2CVVw&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=22)

#### Previous Videos Related to this one

Vagrant Intro [HERE](https://www.youtube.com/watch?v=Vfoj_nu8cmg&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=20)

Ansible Intro [HERE](https://www.youtube.com/watch?v=xT0K0k36pxU&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=19)

Nodejs+Nginx Intro [HERE](https://www.youtube.com/watch?v=6NC5V9gYANs&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=16)


## Key points

- Load balancing using **nginx**
- Launching VMs using **vagrant**
- Configuring the VMs using **ansible**
  - Ansible Roles
  - Templates
  - Variables
  - Handlers
- Simple shell script for manual deployment


## This is what we are going to build

```
       +----------+
       |  Nginx   |
       |  proxy   |
       +----+-----+
            |
            |    Load Balancing
     +------+-------+
     |              |
+----v----+    +----v----+
| NodeJS  |    | NodeJS  |
| VM 1    |    | VM 2    |
+---------+    +---------+
```


### Why Nginx?

- Load balancer
- Caching (Future)
- SSL Termination (Future)
- Advanced rules (Future)

#### Why Load balancer
- Lets us run multiple instances of our app
- Which gives redundancy and fault tolerance.
- Let's us deploy without causing downtime (We can update the backends one at a time)

### Why two VMs

That is only for the purpose of this demonstration. It does not make sense to
have two VMs running just one process each. But I wanted to show the concept
of loadbalancing

## Steps

### 1. Launch the VMs using Vagrant

We have three VMs to launch, obiously we will use Vagrant for that.

Vagrant files [HERE](../infrastructure/vagrant/apps/nodejsapp)



### 2. Write the Ansible manifests to configure the VMs

Ansible files [HERE](../infrastructure/ansible)

We will have these roles

- [common](../infrastructure/ansible/roles/common) : This contains common stuff for all the servers (git, vim etc)
- [nginx-common](../infrastructure/ansible/roles/nginx-common): Whatever that is common for all nginx servers (like, installing nginx itself)
- [nginx-nodejsapp](../infrastructure/ansible/roles/nginx-nodejsapp): nginx stuff specific to our nodejsapp
- [nodejs-common](../infrastructure/ansible/roles/nodejs-common): Common for all nodejs apps

#### On the Nginx VM

We need
    - Nginx installed
    - Nginx virtualhost configuration

#### On the NodeJS VMs

We need
    - NodeJS installed




### 3. Sample application

Of course we need a demo app. This time, we will use an express based simple 
hello world application. Why express? Because I want to introduce `npm install`
as part of our deployment.

The sample app is [HERE](../demo-apps/nodejsapp)

The `package.json` was created using the following. I am leaving it here
for reference, you don't have to do this as the `package.json` is already
present
```
# Just press Enter for all the prompts
npm init
```

And then
```
npm install express --save
```
Which will save the dependency (express) into the `package.json`

### 4. Deploying it

We shall have a simple, dumb script that will do the deployment for us

1. Clone the codebase
2. Run `npm install`
3. Copy the resulting everything into the nodejs machines
4. Restart the node processes

The dumb script is present [HERE](../demo-apps/nodejsapp/deploy.sh)
Please don't use this deploy script for anything other than learning
