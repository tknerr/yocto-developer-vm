
Vagrant.configure("2") do |config|

  # basebox
  config.vm.box = 'generic/ubuntu2004'
  config.vm.box_version = '3.1.6'

  # hostname
  config.vm.hostname = 'yocto-dev-vm'

  # virtualbox specific customizations
  config.vm.provider "virtualbox" do |vbox, override|
    vbox.gui = true
    vbox.name = "Yocto Developer VM"
    vbox.cpus = 8
    vbox.memory = 8192
    vbox.customize ["modifyvm", :id, "--usb", "on"]
    vbox.customize ["modifyvm", :id, "--accelerate3d", "off"]
    vbox.customize ["modifyvm", :id, "--vrde", "off"]
  end

  # vmware specific customizations
  config.vm.provider "vmware_desktop" do |vmware, override|
    vmware.gui = true
    vmware.vmx["displayname"] = "Yocto Developer VM"
    vmware.vmx["numvcpus"] = "8"
    vmware.vmx["memsize"] = "8192"
    vmware.vmx["usb.present"] = "TRUE"
    vmware.vmx["usb.pcislotnumber"] = "33"
    vmware.vmx["usb_xhci.present"] = "TRUE"
  end

  # make sure the current directory is mounted under /vagrant
  config.vm.synced_folder ".", "/vagrant", mount_options: ["ro"]

  # create new login user
  config.vm.provision "shell", privileged: true, path: 'scripts/setup-vm-user.sh',
    args: "user user"

  # run the actual update-vm provisioning script under the new login user
  config.vm.provision "shell", privileged: true, keep_color: true, run: "always", inline: <<-EOF
    sudo -i -u user ROLE_TAGS=#{ENV['ROLE_TAGS']} /vagrant/scripts/update-vm.sh #{ENV['UPDATE_VM_FLAGS']}
    EOF

end
