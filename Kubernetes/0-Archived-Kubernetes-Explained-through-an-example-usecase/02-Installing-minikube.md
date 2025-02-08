# Installing MiniKube

MiniKube is local Kubernetes

1. Install and start Docker Desktop for your operating system
2. Install minikube https://minikube.sigs.k8s.io/docs/start 

## Install Kubectl

Follow instructions https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

## Install JQ

```
sudo apt update
sudo apt install jq
```

## Taking a look around

List all pods across all namespaces
```
mansoor@debian:~$ kubectl get pods -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
kube-system   coredns-668d6bf9bc-85c62           1/1     Running   1 (17m ago)   21m
kube-system   etcd-minikube                      1/1     Running   1 (17m ago)   21m
kube-system   kube-apiserver-minikube            1/1     Running   1 (17m ago)   21m
kube-system   kube-controller-manager-minikube   1/1     Running   1 (17m ago)   21m
kube-system   kube-proxy-8cp4h                   1/1     Running   1 (17m ago)   21m
kube-system   kube-scheduler-minikube            1/1     Running   1 (17m ago)   21m
kube-system   storage-provisioner                1/1     Running   2 (17m ago)   21m
mansoor@debian:~$
```

## Take a look at docker containers

```
mansoor@debian:~$ docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED      STATUS        PORTS
                                                                                             NAMES
002dd4272afb   gcr.io/k8s-minikube/kicbase:v0.0.46   "/usr/local/bin/entr…"   3 days ago   Up 26 hours   127.0.0.1:32768->22/tcp, 127.0.0.1:32769->2376/tcp, 127.0.0.1:32770->5000/tcp, 127.0.0.1:32771->8443/tcp, 127.0.0.1:32772->32443/tcp   minikube
mansoor@debian:~$


mansoor@debian:~$ docker inspect minikube
[
    {
        "Id": "002dd4272afb525456889e2538780878c7d7aa892dadd4d8bfb1141d4a0e9ff2",
        "Created": "2025-01-21T13:04:40.914867389Z",
        "Path": "/usr/local/bin/entrypoint",
        "Args": [
            "/sbin/init"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 1125,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2025-01-24T01:04:22.738561841Z",
            "FinishedAt": "2025-01-24T00:56:58.841429116Z"
        },
        "Image": "sha256:e72c4cbe9b296d8a58fbcae1a7b969fa1cee662cd7b86f2d4efc5e146519cf0a",
```


We can see that the container's process id on the Linux system is 1125

and we do see a process called `/sbin/init` running at that PID
```
mansoor@debian:~$ ps aux|grep 1125
root        1125  0.0  0.3  19892 12568 ?        Ss   Jan23   0:02 /sbin/init
```


Enter the namespace for that process and look at the processes inside that namespace
```
mansoor@debian:~$ sudo nsenter --target 1125 --all
root@minikube:/#
root@minikube:/#
root@minikube:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3  19892 12568 ?        Ss   Jan24   0:02 /sbin/init
root          98  0.0  0.2  23536  9792 ?        S<s  Jan24   0:00 /lib/systemd/systemd-journald
root         144  0.0  0.2  15432  9244 ?        Ss   Jan24   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root         457  0.0  1.4 1949128 58100 ?       Ssl  Jan24   1:19 /usr/bin/containerd
root         740  0.5  2.6 2496648 105344 ?      Ssl  Jan24   8:45 /usr/bin/dockerd -H tcp://0.0.0.0:2376 -H unix:///var/run/docker.sock --default-
root        1039  0.5  1.2 1276308 49580 ?       Ssl  Jan24   8:23 /usr/bin/cri-dockerd --container-runtime-endpoint fd:// --pod-infra-container-im
root        1223  1.4  2.6 2119684 104764 ?      Ssl  Jan24  22:14 /var/lib/minikube/binaries/v1.32.0/kubelet --bootstrap-kubeconfig=/etc/kubernete
root        1492  0.0  0.3 1237940 14408 ?       Sl   Jan24   0:10 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 4081e6e58234a3697018d4f2788
root        1493  0.0  0.3 1237940 13268 ?       Sl   Jan24   0:14 /usr/bin/containerd-shim-runc-v2 -namespace moby -id ca8495891370af63b8aec5d53a0
root        1494  0.0  0.3 1237940 13864 ?       Sl   Jan24   0:08 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 1b9e25d9a375d01dd3838eb4675
root        1495  0.0  0.3 1238196 14280 ?       Sl   Jan24   0:14 /usr/bin/c
```


what if we did `docker ps` inside that namespace. We do see things like `kube-apiserver`
```
root@minikube:/# docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS     NAMES
ebce04ddb356   registry.k8s.io/pause:3.10        "/pause"                 23 minutes ago   Up 23 minutes             k8s_POD_go-hello-world_default_85eab088-a7c9-4d2a-b5b4-013ac1e22a49_0
5af32e09ade3   6e38f40d628d                      "/storage-provisioner"   21 hours ago     Up 21 hours               k8s_storage-provisioner_storage-provisioner_kube-system_50cd78c8-562c-48fa-a52f-26e0feeaa870_5
689290c49c65   c2e17b8d0f4a                      "kube-apiserver --ad…"   21 hours ago     Up 21 hours               k8s_kube-apiserver_kube-apiserver-minikube_kube-system_d72d0a4cf4be077c9919d46b7358a5e8_3
b14728445eab   c69fa2e9cbf5                      "/coredns -conf /etc…"   26 hours ago     Up 26 hours               k8s_coredns_coredns-668d6bf9bc-85c62_kube-system_6d391263-14dc-4c63-be6a-714f7b199569_2
a2f4107b447e   040f9f8aac8c                      "/usr/local/bin/kube…"   26 hours ago     Up 26 hours               k8s_kube-proxy_kube-proxy-8cp4h_kube-system_26bed127-e359-44f8-9768-64673aefbcc5_2
aca58b928112   registry.k8s.io/pause:3.10        "/pause"                 26 hours ago     Up 26 hours               k8s_POD_coredns-668d6bf9bc-85c62_kube-system_6d391263-14dc-4c63-be6a-714f7b199569_2
```