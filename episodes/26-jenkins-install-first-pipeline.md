# Installing and setting up Jenkins - Simple Pipeline Intro

For this, we are not gonna use Docker, we are gonna go the old way and install it on a 
VM


# Installing Jenkins

## Step 1 - Install JDK

```sh
sudo apt update
sudo apt install default-jdk
```

## Step 2 - Add the GPG keys

```
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
```

## Step 3 - Install the package

```
sudo apt update
sudo apt install jenkins
```

## Step 4 - Start and enable

```
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

## Step 5 - Setting up

Visit `server-ip:8080`

Jenkins generates a random password by default. Get the password:
```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
Paste this password into the field

## Step 6 - Installing plugins

At this point, you would want to install the plugins you need. To get started
I would suggest to just install the suggested plugins

## Step 7 - Create the admin user

You know how to fill a form. Create a user. From there it is pretty straight forward

## Step 8 - Configuring Nginx reverse proxy

### Install Nginx
```
sudo apt update
sudo apt install nginx
```

### Create `/etc/nginx/sites-enabled/jenkins.devops.esc.sh`

Change the domain name obviously

```
server {
    listen 80;
    server_name jenkins.devops.esc.sh;

	location / {
		include /etc/nginx/proxy_params;
		proxy_pass          http://localhost:8080;
		proxy_read_timeout  60s;
        # Fix the "It appears that your reverse proxy set up is broken" error.
        # Make sure the domain name is correct
		proxy_redirect      http://localhost:8080 https://jenkins.devops.esc.sh;
	}
}
```
### Verify the config and restart nginx

```
nginx -t
sudo systemctl restart nginx
```

Fix if any syntax error

## Step 9 - Change Jenkins bind address

By default Jenkins listens on all network interfaces. But we need to disable it because
we are using Nginx as a reverse proxy and there is no reason for Jenkins to be exposed
to other network interfaces.

We can change this by editing
`/etc/default/jenkins`

Locate the line starting with `JENKINS_ARGS` (It's usually the last line) and append

```
--httpListenAddress=127.0.0.1
```
So that the line resembles
```
JENKINS_ARGS="--webroot=/var/cache/$NAME/war --httpPort=$HTTP_PORT --httpListenAddress=127.0.0.1"
```

Restart Jenkins
```
sudo systemctl restart jenkins
```
Make sure it is running fine
```
sudo systemctl status jenkins
```

Jenkins should load now, but on http only.

## Step 9 - Configuring SSL

There is a dedicated document for fetching and configuring SSL with Nginx with all the necessary
documents. Go [HERE](24-securing-nginx-free-ssl-letsencrypt.md)

Come back here after that.

Make sure you have the certificate and key in location
```
root@jenkins-server:~# ls -l /etc/letsencrypt/live/jenkins.devops.esc.sh/
total 4
lrwxrwxrwx 1 root root  45 Sep 27 07:52 cert.pem -> ../../archive/jenkins.devops.esc.sh/cert1.pem
lrwxrwxrwx 1 root root  46 Sep 27 07:52 chain.pem -> ../../archive/jenkins.devops.esc.sh/chain1.pem
lrwxrwxrwx 1 root root  50 Sep 27 07:52 fullchain.pem -> ../../archive/jenkins.devops.esc.sh/fullchain1.pem
lrwxrwxrwx 1 root root  48 Sep 27 07:52 privkey.pem -> ../../archive/jenkins.devops.esc.sh/privkey1.pem
-rw-r--r-- 1 root root 692 Sep 27 07:52 README
root@jenkins-server:~#
```


Update the nginx config to look like this
```

server {
    listen 80;
    server_name jenkins.devops.esc.sh;

	location / {
        return 301 https://$host$request_uri;
	}
}

server {
    listen 443 ssl;

    server_name jenkins.devops.esc.sh;

    ssl_certificate /etc/letsencrypt/live/jenkins.devops.esc.sh/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jenkins.devops.esc.sh/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;


    
	location / {
		include /etc/nginx/proxy_params;
		proxy_pass          http://localhost:8080;
		proxy_read_timeout  60s;
        # Fix the "It appears that your reverse proxy set up is broken" error.
        # Make sure the domain name is correct
		proxy_redirect      http://localhost:8080 https://jenkins.devops.esc.sh;
	}
}

```

Make sure nginx is alright `nginx -t`

Reload Nginx

```
sudo systemctl reload nginx
```

And that is pretty much it, Jenkins is up and ready with a freshly configured sweet
sweet green padlocked SSL certificate


## A Simple multi stage pipeline

You can create a pipeline by New Item -> Pipeline. And then in the pipeline definition


```
pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                echo 'building the software'
            }
        }
        stage('test') {
            steps {
                echo 'testing the software'
            }
        }
        stage('deploy') {
            steps {
                echo 'deploying the software'
            }
        }
    }
}
```
