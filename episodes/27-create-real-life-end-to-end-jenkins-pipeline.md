# Creating an end to end Jenkins pipeline for a NodeJS application

So far we have a Jenkins installation up and running. We don't have much else going on.

## Our Goal

We want to automatically test and deploy our NodeJS application. The application is living in a git
repository.

With this video, we will be creating a full pipeline that will:

1. Trigger on a commit to the `develop` or `master` branch
2. Run some tests
3. Deploy it to a development environment or production env depending on the branch



## Our NodeJS app setup

- The app is in a git repository (We will use Github)
- The code runs in two VMs as we did in the past. They have Nodejs installed and configured
- Jenkins runs in another VM


## Steps

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

### 3. Create the Jenkinsfile


### 4. Give Jenkins ssh access to the NodeJS VMs

### 5. Create the Pipeline off of the Jenkinsfile

