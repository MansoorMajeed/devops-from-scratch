# Recap


## Basics of Linux

The idea was that, before we even get started with anything "DevOps", we need to know our
systems well, which is Linux. So it is important to be familiar with the following

1. We started with how the internet works
2. We learned about setting up a Linux VM, accessing it using SSH, Basic commands
3. We dived a bit more deep, learned file descriptors, stdout/stderr etc
4. We continued with file system, env variables, managing users and permissions
5. Managing packages, processes, services etc
6. We learned to edit text files using vim
7. We learned about debugging using ps, netstat, netcat, curl etc


## More about hosting and managing websites

When we work as a DevOps engineer, we mostly work with web applications/services etc.
So it is important for us to understand the concepts, and be familiar with web servers
and the like

1. We learned about Nginx, virtualhosts
2. We learned how DNS and domains work, and how to manage domains
3. We setup a simple static website
4. We proceeded to setup a dynamic website using NodeJS and Nginx reverse proxy
5. We learned about MySQL quite extensively


## Intro to DevOps


Finally it was time to introduce DevOps tools to make our life easier and make things
scale well. So added some tools to the mix where the need arise.
We will continue to add more tools as we need them.

1. We talked about infrastructure as code, configuration management and started with Ansible
2. We learned manage virtual machines using Vagrant
3. We learned about version control, git and github
4. We applied our DevOps lessons and deployed a NodeJS+Nginx app using Ansible
5. We talked about how TLS works and how to setup TLS certificates
6. We spent some time understanding what DevOps is: Agile, Scrum, CI, CD etc
7. We spent some time with Jenkins
8. We setup a bit more complicated web application using WordPress


What is important to understand is, I will not be talking more about Ansible, Jenkins etc
unless we are using them for anything specific. The reasoning is that these tools run
deep and can spend hours talking about them, but if you get an overall idea about what is
going on, you can easily read their documentation and figure out things on your own.

## So, the story so far

If you have watched all the videos so far, I hope you should be knowledgable enough to
run your own little web applications, manage them comfortably, understand the basics of
Linux, the web, some devops concepts etc.

You don't need to know all the tools out there, you just need to know where one fits
and then you should be able to read their respective documentation to figure out things on
your own.

I am here to only give you a framework and fill in the gaps so that you can help yourself much better


## So what is coming?

In the immediate future, we are gonna start with monitoring. Now we have a bunch of systems
to work with, and the next thing is how we use "DevOps" wherever possible
