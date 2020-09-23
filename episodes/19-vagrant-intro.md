# Managing VirtualMachines using Vagrant


Video Link [HERE](https://www.youtube.com/watch?v=Vfoj_nu8cmg&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=20&t=156s)

## The Problem we are trying to solve

We have a lot of VirtualMachines to manage and we don't want to do that manually
We need some sort of a tool to help us with that.

## Installing Vagrant

Follow the [docs](https://www.vagrantup.com/docs/installation)


## Most Basic Vagrantfile

```ruby
Vagrant.configure("2") do |config|

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "base"

end
```

## Multiple VMs with their own IP address, shell provisioning

```ruby
Vagrant.configure("2") do |config|

  config.vm.box = "debian/buster64"


  config.vm.define "nginx" do |nginx|
    nginx.vm.provider "virtualbox" do |vb|
       vb.memory = "512"
    end

    nginx.vm.network "private_network", ip: "192.168.33.10"
    nginx.vm.hostname = 'nginx'

    nginx.vm.provision "shell", inline: <<-SHELL
       apt-get update
       apt-get install -y nginx
    SHELL
  end

  config.vm.define "apache" do |apache|
    apache.vm.provider "virtualbox" do |vb|
       vb.memory = "512"
    end

    apache.vm.network "private_network", ip: "192.168.33.11"
    apache.vm.hostname = 'apache'

    apache.vm.provision "shell", inline: <<-SHELL
       apt-get update
       apt-get install -y apache2
    SHELL
  end
end
```


## Vagrant with ansible provisioning

> Note: If you want to make it work with Windows, you need to do some hacks
> Use google if you would like to do that

### Vagrantfile

```ruby
Vagrant.configure("2") do |config|

  config.vm.box = "debian/buster64"

  config.vm.network "private_network", ip: "192.168.33.10"

 
  config.vm.provider "virtualbox" do |vb|
   
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end
  #

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
end
```

### And the playbook.yml

```yaml
---
- hosts: all

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: installed
```

