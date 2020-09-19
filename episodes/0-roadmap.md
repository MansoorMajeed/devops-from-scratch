
# DevOps From Scratch - RoadMap

This is a roadmap I have planned, and this could change any moment as I continue to make videos


1. How does a simple website work
    1. What is a website. How it works from local machine
    2. What is a server - How does the internet work (IP addresses, Ports etc)
    3. What is DNS (quick intro)
2. Basics of Linux - Setting up simple web server
    1. History of Unix, Linux and the differences
    2. Virtualization - Installing Debian 10 on VirtualBox
    6. SSH - Remote logging, Key Exchange, Key based authentication etc
    7. User management in Linux - quick guide - sudo / root
    8. Installing package using apt-get - nginx
    9. Learn VIM
    10. Starting or stopping services using systemctl
    11. Checking for processes using `ps`
    13. Checking for listening ports using netstat
    14. Checking open ports using netcat from the outside
    15. checking the logs for errors
    16. Before proceeding with nginx config - File system hierarchy in Linux
    17. Nginx configuration - Checking for errors
    18. What is HTTP - what are headers
    19. Host header and virtual hosting in Nginx
3. Getting things onto the internet
    1. Getting a domain, a free domain
    2. Managing DNS for a domain. what it means
    3. Getting our website onto digitalocean server
4. A more complicated web application - WordPress
    1. What is WordPress - what does it need
    2. What is an application server vs web server : [HERE](https://www.nginx.com/resources/glossary/application-server-vs-web-server/)
    3. What is php, php-fpm and why do we need it
    4. What is a database and why do we need it - Intro to MySQL
    5. Installing and setting up WordPress
    6. Scaling wordpress - Why we need LoadBalancers
5. Keeping our files versioned - Git
    1. What is git and why we need it
    2. Basic commands in Git
6. Doing less work with Configuration management - Ansible
    1. What is Configuration management and why do we need it
    2. Basics of ansible
    3. Creating our ansible playbook for our Nginx server
7. Back to a simple nodejs application
    1. This is only for demo - create a very simple app
    2. Keeping it in version control
    3. What is Jenkins, what can it do for us
    4. Automating our deployments - new version gets deployed on git push (Jenkins)
8. Making sure our systems stay up - Monitoring
    1. The need for monitoring, what can it do for us
    2. Installing sensu for simple monitoring (HTTP and process)
9. Getting more serious - Caching
    1. What is caching
    2. More about the HTTP protocol and headers
    3. Caching servers - Nginx
    4. Separate advanced caching with varnish ?
    5. Enable caching for our node application
    6. Automated cache busting as part of deployment
10. Securing our servers with Firewall
    1. What is a firewall and what can it do
    2. Introduction to iptables
11. Keep your stuff backed up
    1. Why we need backup
    2. How to backup individual stuff (MySQL)
12. Evolving to Docker 
    1. What are containers - what are we trying to solve
    2. Installing docker
    3. Getting started with docker containers
    4. Creating our own docker images
    5. Containerizing our node application
    6. Using Jenkins with docker
13. Evolving to Kubernetes
    1. What is Kubernetes - what are we trying to solve
    2. Installing and getting started with minikube
    3. Basics of Kubernetes
    4. Moving our app to Kubernetes
14. Better monitoring with Prometheus
    1. Prometheus, Alertmanager getting started
    2. Plotting our graphs with Grafana
15. Moving to Cloud
    1. What, why of Cloud
16. Google Cloud
17. AWS
18. Creating our infrastructure using Terraform

### Fundamentals of Linux

I have based this on a goal which is to setup a webserver, and learning Linux in the process of doing so.
And the idea goes something like this

To get our website up, we need:
1. A Linux server
  - History of Unix, Birth of Linux
  - Virtualization
  - Install Debian 10 on virtualbox
2. Accessing the server remotely
  - Shell
  - SSH
  - SSH Key exchange - Diffie Hellman Key Exchange concept
  - How key based SSH login is setup
3. Navigating our shiny new server
  - cd, ls etc, basic commands
  - File system structure
4. Creating files and folders
  - echo, mkdir, cat etc
  - vim, nano
5. Create a user for our webserver
  - User management
  - Permissions
6. Installing our webserver
  - Webservers
  - Package management using `apt`
7. Starting our webserver
  - Managing services using `systemctl`
8. Checking if our server works
  - Process management using `ps`, `kill` etc
  - `curl`, `netstat`, `netcat` etc
  - `systemctl status`
9. Configuring Nginx
  - HTTP Headedrs
  - VirtualHost - Creating two virtualhosts
  - Using `/etc/hosts` file
  - Nginx config
  - Checking log files - `tail`, `less`
  - `grep`
10. More useful commands
  - `find`, `lsof`, `df`, `du`, `dig`
11. Basic bash scripting
  - Fundamentals of bash scripting - loops and conditions
  - pipes, sed, awk etc
  - Script to backup our website
  - Script to alert if our website is down
