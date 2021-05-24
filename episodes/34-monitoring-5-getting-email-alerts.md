# VM Monitoring #5 - Receiving email alerts

So far we have been either looking at the sensu dashboard to see the state of the system
or we have been using `sensuctl event list` for that. But this is not very practical as
we cannot always be looking at these. Instead, we should be alerted when something goes wrong.

There are several ways we could be alerted, most prominent ones are:

1. Email
2. Slack messages
3. Phone call (Example: pagerduty)

In this video, we will be setting up email alerts using sensu. So when things go wrong with any of
our services we should get an email alert

## Getting an SMTP provider to send emails

To be able to send emails, we need an SMTP provider. For our use case, we can use GMail itself, which is
free and fairly easy to setup. But, obviously, in a production environment, we would be using some sort of
paid service like mailgun, sendgrid etc.


You can create a new gmail account for this. I created one just to send monitoring emails (for my own servers)

> Note:  If you have 2FA enabled for your gmail account, you need to create an app password

1. Log-in into Gmail with your account
2. Navigate to https://security.google.com/settings/security/apppasswords
3. In 'select app' choose 'custom', give it an arbitrary name and press generate
4. It will give you 16 chars token, you will use it as the password

## Configuring Sensu Email handler

Full sensu docs [HERE](https://docs.sensu.io/sensu-go/latest/observability-pipeline/observe-process/send-email-alerts/)

We discussed what a handler is, it is something that "handles" an event. 

### Get the assets

The `email-handler` let us send emails when things go wrong
```
sensuctl asset add sensu/sensu-email-handler -r email-handler
```

### Add an event filter

Consider the scenario your webserver stopped working. We have our checks running every 15 seconds. And, by default, the handler
will send an email every 15 seconds, until we fix our webserver. We don't want this. This is where event filters help us

We will use the `state_change_only` event filter which will alert only when there is a state change for our event


- If your event status changes from 0 to 1, you will receive one email notification for the change to warning status.
- If your event status stays at 1 for the next hour, you will not receive repeated email notifications during that hour.
- If your event status changes to 2 after 1 hour at 1, you will receive one email notification for the change from warning to critical status.
- If your event status fluctuates between 0, 1, and 2 for the next hour, you will receive one email notification each time the status changes.

Create a file `state-change-only-event-filter.yml`
```
type: EventFilter
api_version: core/v2
metadata:
  annotations: null
  labels: null
  name: state_change_only
  namespace: default
spec:
  action: allow
  expressions:
  - event.check.occurrences == 1
  runtime_assets: []
```

Let's create the event filter
```
sensuctl create -f state-change-only-event-filter.yml
```

### Create the event handler

Create `email-handler.yml`
```
api_version: core/v2
type: Handler
metadata:
  namespace: default
  name: email
spec:
  type: pipe
  command: sensu-email-handler -f <sender@example.com> -t <recipient@example.com> -s <smtp_server@example.com> -u username -p password
  timeout: 10
  filters:
  - is_incident
  - not_silenced
  - state_change_only
  runtime_assets:
  - email-handler
```

We need to update the following

- `-f` : Sender email -> Your new gmail account
- `-t` : Recipient email -> where you want the alerts to go
- `-s` : SMTP Serber -> smtp.gmail.com
- `-u` : Gmail username
- `-p` : Gmail password / app password if you use 2FA for your new account

And create it
```
sensuctl create -f email-handler.yml
```


## Exercises

1. Add email handler to other checks
2. Create a slack message alert handler