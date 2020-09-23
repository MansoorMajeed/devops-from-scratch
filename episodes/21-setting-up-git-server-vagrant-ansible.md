# Setting up a Git server (Using Vagrant and Ansible)

Video Link [HERE](https://www.youtube.com/watch?v=uxE2Le64vHk&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=21)

We are going to setup a local Git server.
The idea is similar even if you are using a cloud provider.

**Vagrant** will be used to provision the VM. Vagrantfile is [HERE](../infrastructure/vagrant/apps/git-server/Vagrantfile)

**Ansible** will be used to fully automate the management of the git server.
Ansible files are [HERE](../infrastructure/ansible)

The git-server specific role which has all the stuff needed for the git server is [HERE](../infrastructure/ansible/roles/git-server)

## Steps for manually doing it

It's pretty simple.

1. Launch a VM (or a cloud server depending on where you are doing it)
2. Create a `git` user. This user will be used for all the git operations
3. Install git
4. Give access to your ssh keys

## Automating it

1. Create Vagrantfile to launch the VM
2. Write the Ansible role to do everything that is needed
	- Install the package `git`
	- Create the `git` user
	- Manage SSH keys to give access to the repo
	- Manage repositories
3. Make a prettier DNS address for the git server
