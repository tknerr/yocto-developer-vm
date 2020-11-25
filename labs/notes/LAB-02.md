
# Lab 2: Advanced Yocto configuration

## Lab 2 - Add Packages to the RootFS

As always, make sure you have the environment set up (last time I repeat it ;-)):
```bash
cd ~/yocto-labs
source poky/oe-init-build-env
```

In `conf/local.conf`, add the dropbear package:
```bash
echo 'IMAGE_INSTALL_append = " dropbear"' >> conf/local.conf
```

Then re-create the rootfs image:
```bash
bitbake core-image-minimal
```

Finally, mount the SD card again (see [LAB-01](./LAB-01.md)) and ovrwrite the rootfs partition:
```bash
# mount the SD card
sudo mount /dev/sdc2 /media/$USER/rootfs

# overwrite the rootfs
sudo rm -rf /media/$USER/rootfs/**
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/beaglebone/core-image-minimal-beaglebone.tar.xz -C /media/$USER/rootfs

# write caches to disk
sudo sync

# unmount the SD card
sudo umount /dev/sdc2
```

Next:
* insert the SD card back into BBB
* boot from the SD card (power-off, press button, power-on)
* in case of any stack trace -- try the reset button (sometimes it won't work correctly on first boot)


## Lab 2 - Setup NFS Server

Goal of this lab was to setup an NFS server on the VM so that the BBB would boot from the rootfs on the NFS share for faster turnaround times.

I did not do that yet, so this is TBD...

Notes:
* network adapter is eth1 on VM and on BBB its eth0
