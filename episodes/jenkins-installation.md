# Installing and setting up Jenkins

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

### Prerequisites

- Make sure the domain is pointed to the server IP
- The server is publicly accessible over port 80

https://www.digitalocean.com/community/tutorials/how-to-configure-jenkins-with-ssl-using-an-nginx-reverse-proxy-on-ubuntu-20-04
