# A Practical Example of What containers can do

Before we learn in deep about containers, I want to take a minute to show you what we can do with it. I believe this will give an overall idea about the reason why we are learning about containers


## Our Requirement

For this example, let's say that we have the same [NodeJS application](https://github.com/MansoorMajeed/devops-nodejs-demo-app) we have used in the past. We want to deploy this application (we will simply deploy it on our local machine)


## Setting it up the old way -  without containers


### 1. Clone the repo

```
git clone https://github.com/MansoorMajeed/devops-nodejs-demo-app.git
```

### 2. Installing the dependencies

In this case, the application is pretty simple. It does not have too many dependencies. But we still need to install a few things


1. NodeJS and NPM
3. All the libraries and dependencies our application will use

In a more complex situation, we might need a database, a caching server, another api app, etc etc. So, we have to install all of those dependencies (most of the time, a specific version of each) and binaries on our laptop.

For this example, let's use [NVM](https://github.com/nvm-sh/nvm) to install NodeJS and NPM. After that, execute `npm install` within the directory.

Finally, we should be able to run our application using `node index.js` from the same directory

## A better way to deal with it - with containers

First of all, the application still need all of the dependencies, libraries etc. But, if we can find a way to package it all together and send this single "package" around, we don't need to worry about any of it. Right? That is the core idea behind containers

For that, we would need some sort of configuration that says what are all the packages and dependencies we will need with our application.

Let's say our configuration looks like this

> **Note**: This is a hypothetical configuration for illustrative purposes.

```
Steps:
 1. Install NodeJS version we need : package install nodejs-18
 2. Install all the modules : npm install
 3. Copy all of our application code and dependencies: copy ./* destination-package
```


Now that we have this `configuration` file, we can use this to create our `package` that contains our application and everything it needs.

Let's say that it creates a package called `nodejs-demo-app`, we should be able to run it easily using some sort of command. Maybe something like

```
mycontainer-tool run nodejs-demo-app
```

And that is exactly what we are able to do.

### Creating the "package"

First we have to write something called a "Dockerfile". Now, don't even worry about what "Docker" or any of it is, we will definitely get to it. for now you can just ignore it and just focus on the idea of it.

So we create a file called `Dockerfile` in the same location where we have our application code

```➜  devops-nodejs-demo-app git:(master) ✗ pwd
/home/mansoor/git/github.com/mansoormajeed/devops-nodejs-demo-app

➜  devops-nodejs-demo-app git:(master) ✗ ls -l
total 80
-rw-r--r--. 1 mansoor mansoor   447 Aug 13 16:53 deploy.sh
-rw-r--r--. 1 mansoor mansoor   109 Aug 13 17:10 Dockerfile
-rw-r--r--. 1 mansoor mansoor   473 Aug 13 16:53 index.js
-rw-r--r--. 1 mansoor mansoor  1309 Aug 13 16:53 Jenkinsfile
drwxr-xr-x. 1 mansoor mansoor  2478 Aug 13 16:58 node_modules
-rw-r--r--. 1 mansoor mansoor   367 Aug 13 16:53 package.json
-rw-r--r--. 1 mansoor mansoor 55700 Aug 13 16:58 package-lock.json
-rw-r--r--. 1 mansoor mansoor   207 Aug 13 16:53 README.md
drwxr-xr-x. 1 mansoor mansoor    14 Aug 13 16:53 test
➜  devops-nodejs-demo-app git:(master) ✗

```

And the content of the Dockerfile
```
FROM node 

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY index.js ./

CMD ["node", "index.js"]
```

Don't worry about the syntax, but as you can see, it is very simple and makes total sense, right?

Now, we simply run the magic command that creates the package

We run `docker build -t nodejs-demo-app .`

(Don't forget the `.` at the end)

Once that is done, we should see 
```
 => exporting to image                                                           
 => => exporting layers                                                          
 => => writing image sha256:4e95496b68f87af00ee40230da330da222f5960830b0b276aa0925147ee685c8 
 => => naming to docker.io/library/nodejs-demo-app
```

And now we can run
```
docker run -p 3000:3000 nodejs-demo-app
```
Here, the only thing that might look odd is the `-p 3000:3000`,  that is simply us telling Docker to expose port number 3000 from the container to our host machine's port 3000. This way we can reach our application from our laptop.

And finally, we can access our app, from a terminal on our laptop
```
curl localhost:3000

<h1>Hello World!</h1>
   <h2>
    Process ID: 1 <br>
    Running on: 2ab5e19ef284 <br>
    App Version: 4.0
   </h2>
```


