# Containerizing a Golang App

We will dockerize a basic golang app. We will use [THIS](https://github.com/MansoorMajeed/go-hello-world) for this part


## Installing Docker on Debian

If no sudo. Do this and logout and login
```
apt update
apt install sudo
usermod -aG sudo yourusername
```

Install Docker
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER

newgrp docker
```


## Write the Dockerfile

Simplest dockerfile for a Golang app
```
FROM golang:latest AS builder

WORKDIR /app

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Second stage: Create a smaller image
FROM scratch

# Copy the binary from the builder stage
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
```

## Build and run

Commands to build the image
```
docker build -t go-hello-world:0.1 .
```

and to run
```
docker run image
```

