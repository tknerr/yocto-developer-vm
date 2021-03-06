# Lab 5: Extend a recipe

## Lab 5 - Overview

Several steps are involved in this lab, so here is a brief overview:

1. Create BBAppend File for linux-ti-staging Kernel
2. Apply Kernel Patches to support Nunchuk
3. Wiring and Testing the Nunchuk
4. Patching nInvaders Game for Nunchuk input device

## Lab 5 - Create BBAppend File for linux-ti-staging Kernel

Create an exemplary .bbappend file for `meta-ti/recipes-kernel/linux/linux-ti-staging_5.4.bb` in `meta-zuehlkelabs/recipes-kernel/linux/linux-ti-staging_5.4.bbappend` 

Run `bitbake-layers show-appends | grep -B1 zuehlke` and verify you see this in the output:
```
linux-ti-staging_5.4.bb:
  /home/user/yocto-labs/meta-zuehlkelabs/recipes-kernel/linux/linux-ti-staging_5.4.bbappend
```

=> this shows that our .bbappend file got hooked in successfully and will be respected the next time linux-ti-staging is baked.

## Lab 5 - Apply Kernel Patches to support Nunchuk

The kernel needs to be patched in order to support the nunchuk drivers. We do that by adding the patches via .bbappend file created above in `meta-zuehlkelabs/recipes-kernel/` and re-building the virtual/kernel recipe:

 * Add the patch files from `zuehlke-lab-data/nunchuk/linux/*` to `meta-zuehlkelabs/recipes-kernel/linux-ti-staging-5.4/`
 * Note: the patch files could by convention should reside in
    - either `files/` (generic)
    - or `linux-ti-staging-5.4/` (version specific)
    - or `linux-ti-staging-5.4/beaglebone` (version and machine specific)

Once the .patch files have been added, make sure the are included in `meta-zuehlkelabs/recipes-kernel/linux-ti-staging_5.4.bbappend`:
```
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-5.4:"

SRC_URI += "file://0001-Add-nunchuk-driver.patch \
            file://0002-Add-i2c1-and-nunchuk-nodes-in-dts.patch \
            file://defconfig \
           "
```

Then make sure to clean and rebuild the "linux-ti-staging" and "virtual/kernel" recipes:
```bash
# clean
bitbake -c clean linux-ti-staging
bitbake -c cleansstate linux-ti-staging
bitbake -c clean virtual/kernel
bitbake -c cleansstate virtual/kernel

# build
bitbake linux-ti-staging
bitbake virtual/kernel
```

Next:
* shutdown BBB and remove SD card
* insert SD card into reader (it should auto-mount, otherwise see instructions in [LAB-01](./LAB-01.md))

Due to the updated kernel / drivers you also need to copy over dtb and zImage to the boot/ partition (in addition to the rootfs, which needs to be updated as well):
```bash
# copy kernel and device tree
sudo cp ~/yocto-labs/build/tmp/deploy/images/beaglebone/zImage /media/$USER/boot/zImage
sudo cp ~/yocto-labs/build/tmp/deploy/images/beaglebone/am335x-boneblack.dtb /media/$USER/boot/dtb

# overwrite the rootfs
sudo rm -rf /media/$USER/rootfs/**
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/beaglebone/core-image-minimal-beaglebone.tar.xz -C /media/$USER/rootfs
```

Next:
* sync and unmount the SD card
* place the SD card back into BBB
* boot the BBB from the SD card again

After booting finished, check if WII mode is enabled via picocom:
```
zcat /proc/config.gz | grep "WII"
```

You should see "CONFIG_JOYSTICK_WIICHUCK=y" in the output:
```
root@beaglebone:~# zcat /proc/config.gz | grep "WII"
CONFIG_JOYSTICK_WIICHUCK=y
# CONFIG_HID_WIIMOTE is not set
```

Also, you should see the "event0" and "js0" input devices:
```bash
ls -la /dev/input/
```

## Lab 5 - Wiring and Testing the Nunchuk

We need to wire the Nunchuk with the BBB.

Next:
 * make sure the BBB is turned off (run `halt` from within the BBB, then unplug power)
 * follow the steps / pictures in the labs in order to correctly wire the Nunchuk with the BBB
 * See also GPIO pin reference for the BBB: https://www.mathworks.com/help/supportpkg/beagleboneio/ug/the-beaglebone-black-gpio-pins.html

After wiring the Nunchuk with the BBB, you should also see it getting connected in the boot log output:
```
...
[    2.329689] udevd[89]: starting eudev-3.2.9
[    2.712615] wiichuck 1-0052: Connected Nunchuk
[    4.813572] EXT4-fs (mmcblk0p2): re-mounted. Opts: (null)
...
```

You should also be able to read from the `/dev/input/event0` or `/dev/input/js0` devices.
Note: output will look garbled as it's binary data, but at least you should see that input
is generated by the Nunchuk when interacting with the accelerometer / joystick / buttons.

* use `cat /dev/input/event0` to verify the Nunchuk is working


## Lab 5 - Patching nInvaders Game for Nunchuk input device

Before we can play nInavers via Nunchuk, we need to patch it as well:
 * add the patch file from `zuehlke-lab-data/nunchuk/ninvaders/joystick-support.patch`
 * reference the patch file via `SRC_URI`

After copying the patch file to `meta-zuehlkelabs/recipes-games/ninvaders/files/`, we can simply reference it in `ninvaders_0.1.1.bb` like so:
```
...
# patch nInvaders.c to use joystick support
SRC_URI += "file://joystick-support.patch"
```

Next:
* run `bitbake ninvaders` to rebuild the recipe
* if successful, run `bitbake core-image-minimal` to rebuild the rootfs
* update the rootfs on the SD card

After reboot with the updated SD card in the BBB, you should be able to play `nInvaders` with the Nunchuk:
* use joystick to navigate left/right
* use top button to fire missile