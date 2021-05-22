# VM Monitoring #4 - Monitoring a webserver using Sensu

Monitoring only system resources is not enough, it is possible for our services to fail without
any problem with system resources. Example, Nginx could crash, MySQL could stop working etc even when
the system is doing fine otherwise.

To be alerted of these, we need to monitor
1. Whether a process is running (nginx, mysql etc)
2. Whether the service is responding on their respective ports (80,443 for nginx, 3306 for mysql)

So we will create checks for these

## Monitoring running processes

In this case, we have two processes that we want to monitor : Nginx and MySQL

Both are already installed on our `wordpress` server. If you do not have them, go ahead and install them.

### Fetch assets

We will use the [nagiosfoundation](https://bonsai.sensu.io/assets/ncr-devops-platform/nagiosfoundation) plugin to monitor
running processes

```
sensuctl asset add ncr-devops-platform/nagiosfoundation -r nagiosfoundation
```

### Update subscription

```
sensuctl entity list
sensuctl entity update wordpress
```

    For Entity Class, press enter.
    For Subscriptions, type system,webserver and press enter.


### Create check

```
sensuctl check create nginx_service \
--command 'check_service --name nginx' \
--interval 15 \
--subscriptions webserver \
--runtime-assets nagiosfoundation
```

We should see the event in few seconds
```
sensuctl event list
```

Go ahead and stop Nginx and see what happens in sensu

## Doing an http check

Previously we were checking if the process was running. But this is not enough. It is possible
for nginx to be running and still unresponsive. So, we need a check that does an actual http
request

### Fetch assets

We will use https://bonsai.sensu.io/assets/sensu-plugins/sensu-plugins-http for that
```
sensuctl asset add sensu-plugins/sensu-plugins-http:6.0.0 -r sensu-plugins-http
```

We have already added the ruby runtime in the past, if you have not done that, make sure that asset is also added
```
sensuctl asset add sensu/sensu-ruby-runtime:0.1.0 -r sensu-ruby-runtime
```

### Create check


```
sensuctl check create nginx_http \
--command 'check-http.rb -u http://localhost' \
--interval 15 \
--subscriptions webserver \
--runtime-assets sensu-plugins-http,sensu-ruby-runtime 
```


### Verify

```
sensuctl event list
```


## Exercises

1. Create a check to monitor if mysql is running
1. Create a check to connect to mysql database
