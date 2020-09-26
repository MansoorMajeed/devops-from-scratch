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

## Step 9 - Configuring SSL
