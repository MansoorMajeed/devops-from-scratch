# How does the internet work

Video Link : [E1](https://www.youtube.com/watch?v=SyPzQrUxmZc&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=3&t=0s)


## What is a website

A webpage is nothing but a document on the internet
you can access.

This is a webpage
```html
<h1>Hello there</h1>
```
A website is a collection of web pages. It could have images, videos etc too. You get the idea

## What is a Network

Computers connected together.

### Why do we need a Network?

So that we can share documents, media, resources like printer etc. This means we can share our
simple website in the network too.

### Types of network

1. Local Area Network (LAN) : Consists of a small number of devices. Example: WiFi network at home
2. Wide Area Network (WAN) : A giant network, connecting other networks, devices etc.

## What is the Internet

Internet is nothing but a network of networks. Your home wifi network is connected to the ISP.
And the ISP connects you to the other parts of the internet managed by your ISP.
And the ISPs connect to each other through high speed network such as the backbone network

## What is a server

In theory, a server is no different than the computer you have. They only differs in what software
they might have installed and the hardware components like how many cores of CPUs of how many GBs
of memory they have

## IP Addresses

A unique identifier for a device in a network.
There is more to learn here.

## Port Numbers

If IP address is an address to a house, you can think of port numbers as windows or doors to your house

In a real example, an IP address means an address to a unique computer in a network
and port numbers means different logical windows in the same computer. This helps us to
have multiple services to run and listen on the same computer

For example, if you have a web server, it listens on port number 80
If you have an SSH server, it listens on 22

### What does "listen" mean

It means, the services is listening in a window (port) for any request to come to that port.
Think of it like a check-in counter at the airport. The staff waits until a traveller arrives at that
window and then he/she proceeds to handle the traveller

## What are Protocols

Protocols are rules on how to talk to each other.
For example, if you want to talk to someone in English, you both should know the rules of the English
language. Protocols are like that. All the computers talking to each other using a language should follow
certain rules.

For example, if you are building a webserver, it should follow certain rules so that the browser can
actually read the page you are serving. The browser already follows those rules.

## What is DNS

DNS stands for Domain Name System. It is a system to translate domain names (example esc.sh or google.com) to
IP addresses.

### Why do we need to do that?

Because computers talk to each other using IP addresses. Domain names such as google.com is there for our
convenience. For example, when your browser is talking to www.google.com, the first thing it needs to do
is to find out the IP address of www.google.com

[More on DNS later]

## For more research

These are the topics that you could research on your own

1. OSI Model, TCP/IP Model. Why are they important
2. Most used ports
3. IP Subnetting
4. How does the packet gets routed through the internet - Routing protocols
5. How does a router work
6. Network Address Translation
7. IPV4 vs IPV6
8. TCP vs UDP
9. AS Numbers, BGP
