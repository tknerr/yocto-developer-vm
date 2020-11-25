
# Yocto Developer VM

Ansible-managed Linux Developer VM for the [Yocto Training](https://bootlin.com/training/yocto) / Workshop, based on https://github.com/Zuehlke/linux-developer-vm-with-ansible.

![Yocto Developer VM Screenshot](https://user-images.githubusercontent.com/365744/100019526-7c84ce00-2dde-11eb-98ce-ad250d8ddf24.png)

## What's included?

### Main tools

These are the main tools included in this developer VM:

 * [Toolchain](https://github.com/tknerr/yocto-developer-vm/blob/feature/yocto-dev-vm/roles/toolchain/tasks/main.yml) - basic toolchain with prerequisites for building yocto images
 * [VSCode](https://github.com/microsoft/vscode) - a general purpose text editor
 * [Picocom](https://github.com/npat-efault/picocom) - terminal emulator for grabbing the serial connection output

Apart from the above, the following tools are used to set up and maintain this developer VM:

 * [Ansible](https://docs.ansible.com/ansible/latest/index.html) - for managing / installing this developer VM
 * [Ansible-lint](https://github.com/ansible/ansible-lint) - to ensure best practices when adding more Ansible roles
 * [TestInfra](https://testinfra.readthedocs.io/en/latest/) - for verifying that the developer VM is set up correctly

## Usage

### Obtaining and Starting the VM Image

Simply run `vagrant up` in order to bring up the Yocto Developer VM (might take a while), then log in with:

 * username: "user"
 * password: "user"

From then on just open a terminal and you will have all of the tools available (see "What's included?").

### Labs and Exercises

You can find the lab materials here (note: they are also available via `/vagrant/labs/content/` from within the VM:

* the original [lab contents](https://github.com/tknerr/yocto-developer-vm/tree/feature/yocto-dev-vm/labs/content) (slides, exercises, lab material)
* the [lab notes](https://github.com/tknerr/yocto-developer-vm/tree/feature/yocto-dev-vm/labs/notes) I have taken during the workshop

*NOTE: Training materials are created by Bootlin and shared under [Creative Commons Attribution - Share Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode) licencse. The sources for the training materials can be found at https://github.com/bootlin/training-materials/*

### Updating the VM

You can run these commands from anywhere inside the developer VM:

 * `update-vm` - update the VM by applying the Ansible roles from the locally checked out repo at `~/vm-setup`
 * `update-vm --pull` - same as above, but update repo before by pulling the latest changes
 * `update-vm --verify-only` - don't update the VM, only run the TestInfra tests
 * `update-vm --provision-only` - don't run the TestInfra tests, only update the vm

### Further Usage Instructions

For general instructions, please refer to the README.md that is placed on the Desktop of the Developer VM:

* [roles/readme/files/README.md](./roles/readme/files/README.md)


## Building and Packaging the VM

### Prerequisites

You only need [VMware Workstation](https://www.vmware.com/products/workstation-pro.html) / [VirtualBox](http://virtualbox.org/wiki/Downloads) and [Vagrant](http://www.vagrantup.com/)
installed.

All other requirements, including Ansible will be installed *inside the Vagrant VM* during provisioning, i.e. you don't need them installed on your host machine.

### Building

Bring up the developer VM:
```
$ vagrant up
```

This will take a while, as it will do quite a few things inside the VM:

 1. set up a new user account using the `setup-vm-user.sh` script
 1. update the VM using `update-vm.sh` script
    1. installs Ansible from PyPi
    1. runs the `site.yml` playbook to install the toolchain and configure the developer VM
    1. checks the roles via `ansible-lint` to ensure best practices
    1. verifies the configuration of the VM via TestInfra 

Watch the vagrant output on the console for seeing progress. At the end you
should see all tests passing:

```
...
    default: ============================= test session starts ==============================
    default: platform linux -- Python 3.8.2, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python3
    default: cachedir: .pytest_cache
    default: rootdir: /home/user/vm-setup
    default: plugins: testinfra-5.0.0, spec-2.0.0
    default: collecting ...
    default: collected 8 items
    default:
    default: spec/test_ansible.py:
    default: ✓ Ansible is installed at version 2 9 6 [local]
    default: ✓ Ansible commands are found [local]
    default: ✓ Ansible version command reports version 2 9 6 [local]
    default:
    default: spec/test_ansible_lint.py:
    default: ✓ Ansible lint is installed at version 4 2 0 [local]
    default: ✓ Ansible lint command is found [local]
    default: ✓ Ansible lint version command reports version 4 2 0 [local]
    default:
    default: spec/test_testinfra.py:
    default: ✓ Testinfra is installed at version 5 0 0 [local]
    default: ✓ Pytest spec is installed at version 2 0 0 [local]
    default:
    default: ============================== 8 passed in 4.05s ===============================
```

If these are passing as expected, you can continue developing on the Ansible roles within this repo.
Please don't forget to add a test for each new feature you add (see "Contributing")

### Packaging

Whenever you feel like distributing a fat VM image rather than a Vagrantfile,
you can package / export it as a VirtualBox image. This might be useful
for distributing the initial version of the developer VM to your dev team,
or simply for preserving checkpoint releases as a binary images.

Let's start from a clean state:
```
$ vagrant destroy -f
$ vagrant up
```

This will provision the VM as usual. Once the provisioning succeeded, we will
do a few cleanup steps before packaging the VM.

First, unmount the /vagrant shared folder:
```
$ vagrant ssh -c "sudo umount /vagrant -f"
```

Then remove the vagrant user account:
```
$ vagrant ssh -c "sudo pkill -KILL -u vagrant"
$ vagrant ssh -c "sudo userdel -f -r vagrant"
```

Finally, shutdown the VM, remove the sharedfolder, and export the VM as an .ova file

For VirtualBox:
```
$ vagrant halt
$ VBoxManage sharedfolder remove "Yocto Developer VM" --name "vagrant"
$ VBoxManage modifyvm "Yocto Developer VM" --name "Yocto Developer VM v0.1.0"
$ VBoxManage export "Yocto Developer VM v0.1.0" --output "yocto-developer-vm-v0.1.0.ova" --options manifest,nomacs
```

For VMware:
```
$ vagrant halt
$ VMX_FILE=`cat .vagrant/machines/default/vmware_desktop/id`
$ ovftool --name="Yocto Developer VM v0.1.0" "$VMX_FILE" yocto-developer-vm-v0.1.0.ova
```

Don't forget to throw away the VM when you are done:
```
$ vagrant destroy -f
```

## Contributing

 1. Fork the repository on Github
 1. Create a named feature branch (like `feature/add-xyz`)
 1. Implement your changes, add tests
 1. Commit and push
 1. Submit a Pull Request via Github
