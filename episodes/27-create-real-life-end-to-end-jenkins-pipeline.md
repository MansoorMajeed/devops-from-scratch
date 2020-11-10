# Creating an end to end Jenkins pipeline for a NodeJS application

So far we have a Jenkins installation up and running. We don't have much else going on.

## Our Goal

We want to automatically test and deploy our [NodeJS application](https://github.com/MansoorMajeed/devops-nodejs-demo-app). The application is living in a git
repository.

With this video, we will be creating a full pipeline that will:

1. Trigger on a commit to the `master` branch
2. Run some tests
3. Deploy it


## Our NodeJS app setup

- The app is in a git repository (We will use Github)
- The code runs in two VMs as we did in the past. They have Nodejs installed and configured
- Jenkins runs in another VM

Before we automate our deploys, first let's make sure that it works fine doing manually

### 1. Review Current setup


The NodeJS demo app is here https://github.com/MansoorMajeed/devops-nodejs-demo-app

This is our original deploy script

```bash
#!/bin/bash


npm install

# For the love of all that is good, don't use this in production
# This is only for a demonstration of how things work behind the scene

ssh vagrant@192.168.33.11 'sudo mkdir -p /app; sudo chown -R vagrant. /app'
rsync -avz ./ vagrant@192.168.33.11:/app/
ssh vagrant@192.168.33.11 "sudo pkill node; cd /app; node index.js > output.log 2>&1 &"


ssh vagrant@192.168.33.12 'sudo mkdir -p /app; sudo chown -R vagrant. /app'
rsync -avz ./ vagrant@192.168.33.12:/app/
ssh vagrant@192.168.33.12 "sudo pkill node; cd /app; node index.js > output.log 2>&1 &"
```

### 2. Make the deploy process better

Here, we were using very basic and stupid way to manage our node processes. We need to change that.
Instead of killing and starting the node process manually, we can ask systemd to do that for us.
Then we can start/stop/restart our process using `systemctl restart ourappname`

So, let's create systemd service file on both the NodeJS Vms

Create `/lib/systemd/system/nodeapp.service`

```
[Unit]
Description=DevOps From Scratch Demo NodeJS App
Documentation=https://esc.sh
After=network.target

[Service]
Type=simple
User=vagrant
WorkingDirectory=/app
ExecStart=/usr/bin/node /app/index.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

And once that is done, let's make these changes into effect

```
systemctl daemon-reload
```

Now the deploy script becomes

```bash
#!/bin/bash


npm install

# For the love of all that is good, don't use this in production
# This is only for a demonstration of how things work behind the scene

ssh vagrant@192.168.33.11 'sudo mkdir -p /app; sudo chown -R vagrant. /app'
rsync -avz ./ vagrant@192.168.33.11:/app/
ssh vagrant@192.168.33.11 "sudo systemctl restart nodeapp"


ssh vagrant@192.168.33.12 'sudo mkdir -p /app; sudo chown -R vagrant. /app'
rsync -avz ./ vagrant@192.168.33.12:/app/
ssh vagrant@192.168.33.12 "sudo systemctl restart nodeapp"
```

Much better


## Make our app get automatically deployed on any change


### 1. Create ssh key for our Jenkins server

Because Jenkins needs to access git and the NodeJS VM through ssh, we will need an ssh key for Jenkins

Run this anywhere we can copy the key from:

I am gonna run this from my Mac laptop

```
ssh-keygen -t rsa -b 4096 -C "jenkins@local" -f ./jenkins_id_rsa
```

This will create the keypair in the same directory
```
ls -l jenkins_id_rsa*
-rw------- 1 mansoor 3381 Oct 24 09:44 jenkins_id_rsa
-rw-r--r-- 1 mansoor  739 Oct 24 09:44 jenkins_id_rsa.pub
```

### 1. Give Jenkins access to the Git repository

Because we want to be able to poll for changes and pull code from there. This is fine if the repository
is a public one, but we are going to go ahead and add the credentials because in a real scenario, most
of the time it will be a private repo


Also, we need to make sure that `git` is installed on the Jenkins server
```
sudo apt install git
```

> Note: new repositories in Github now uses "main" instead of "master", but for now let's stick to "master"

Create new repository -> Settings -> Deploy Key -> Add our new public key there

### 2. Install NodeJS on the jenkins server

Because we are using the same Jenkins master server to do the build/deploy and for our NodeJS app, we have
to run `npm install`, we need to install NodeJS on the Jenkins server

I will make the Ansible playbook to install it automatically and share it, for now, let's install it
manually

On Jenkins server
```
curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt-get install -y nodejs gcc g++ make
```

### 3. Create the Jenkinsfile in the app repository

```
pipeline {
    agent any

      stages {
          stage('build') {
              steps {
                  echo 'building the software'
                  sh 'npm install'
              }
          }
          stage('test') {
              steps {
                  echo 'testing the software'
                  sh 'npm test'
              }
          }

          stage('deploy') {
              steps {
                withCredentials([sshUserPrivateKey(credentialsId: "jenkins-ssh", keyFileVariable: 'sshkey')]){
                  echo 'deploying the software'
                  sh '''#!/bin/bash
                  echo "Creating .ssh"
                  mkdir -p /var/lib/jenkins/.ssh
                  ssh-keyscan 192.168.33.11 >> /var/lib/jenkins/.ssh/known_hosts
                  ssh-keyscan 192.168.33.12 >> /var/lib/jenkins/.ssh/known_hosts

                  rsync -avz --exclude  '.git' --delete -e "ssh -i $sshkey" ./ vagrant@192.168.33.11:/app/
                  rsync -avz --exclude  '.git' --delete -e "ssh -i $sshkey" ./ vagrant@192.168.33.12:/app/

                  ssh -i $sshkey vagrant@192.168.33.11 "sudo systemctl restart nodeapp"
                  ssh -i $sshkey vagrant@192.168.33.12 "sudo systemctl restart nodeapp"

                  '''
              }
          }
      }
    }
}

```

### 4. Give Jenkins ssh access to the NodeJS VMs

Because we will be using SSH to do the deploys, the Jenkins VM should be able to access the NodeJS VMs

### 5. Create the Pipeline off of the Jenkinsfile

