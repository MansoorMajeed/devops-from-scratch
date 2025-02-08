# Running our service as a pod


This will create a simple pod that runs our service. We'll use the following YAML file to define the pod:
```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: go-hello-world
  labels: 
    app: go-hello-world
spec: 
  containers: 
  - name: go-hello-world
    image: gcr.io/google-samples/hello-app:1.0
    ports: 
    - containerPort: 8080
```


## Seeing the pod as a container

```
mansoor@debian:~$ sudo nsenter --target 1125 --all
root@minikube:/# docker ps | grep hello
0699989587bf   gcr.io/google-samples/hello-app   "/hello-app"             26 minutes ago   Up 26 minutes             k8s_go-hello-world_go-hello-world_default_85eab088-a7c9-4d2a-b5b4-013ac1e22a49_0
ebce04ddb356   registry.k8s.io/pause:3.10        "/pause"                 27 minutes ago   Up 27 minutes             k8s_POD_go-hello-world_default_85eab088-a7c9-4d2a-b5b4-013ac1e22a49_0
root@minikube:/#
```