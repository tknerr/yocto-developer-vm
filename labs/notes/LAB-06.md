# Yocto Training Notes 2020-11-24

## Lab 6 - Create a Custom Machine

### Overview

In this exercise, we:
 1. create new machine config `meta-zuehlkelabs/conf/machine/zuehlkelabs.conf` and configure it (see below)
 2. add layer dependency from "meta-zuehlkelabs" to "meta-ti"
 3. set `MACHINE = "zuehlkelabs"` in `build/conf/local.conf`
 4. rebuild the "core-image-minimal" (outputs will be created in `build/tmp/deploy/images/zuehlkelabs/` now)
 5. copy kernel, bootloader, rootfs files to SD card and reboot BBB

### Step-by-Step

Create the "zuehlkelabs" machine config, based on instructions given in the lab exercise:
 * this was done mostly by looking at the existing `meta-ti/conf/machine/beaglebone.conf`
 * ...and the included `meta-ti/conf/machine/include/ti33x.conf`

Resulting `meta-zuehlkelabs/conf/machine/zuehlkelabs.conf`:
```
#@TYPE: Machine
#@NAME: ZuehlkeLabs machine
#@DESCRIPTION: Machine configuration for the ZuehleLabs BBB

require conf/machine/include/ti-soc.inc

# Processor
DEFAULTTUNE = "armv7athf-neon"
require conf/machine/include/tune-cortexa8.inc

# Kernel
PREFERRED_PROVIDER_virtual/kernel = "linux-ti-staging"
KERNEL_DEVICETREE = "am335x-boneblack.dtb"
KERNEL_IMAGETYPE = "zImage"

# Bootloader
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-ti-staging"
UBOOT_ARCH = "arm"
UBOOT_MACHINE = "am335x_evm_config"
UBOOT_ENTRYPOINT = "0x80008000"
UBOOT_LOADADDRESS = "0x80008000"

# include u-boot in image build
EXTRA_IMAGEDEPENDS += "u-boot"

# Serial console
SERIAL_CONSOLES = "115200;ttyS0"

# List common SoC features
MACHINE_FEATURES = "apm usbgadget usbhost vfat ext2 alsa"
```

Also, we should update our layer dependencies properly in `meta-zuehlelabs/conf/layer.conf` to reflect our dependency on the "meta-ti" layer:
```
...
LAYERDEPENDS_meta-zuehlkelabs = "core meta-ti"
...
```

Before rebuilding the image, we need to change the `MACHINE` to "zuehlkelabs" in `build/conf/local.conf`:
```
...
MACHINE = "zuehlkelabs"
...
```

Now, we can rebuild the image:
* create image as usual: `bitbake core-image-minimal`
* review the output (from **"zuehlkelabs" directory**): `ls build/tmp/deploy/images/zuehlkelabs/`

Next:
* shutdown BBB and remove SD card
* insert SD card into reader (it should auto-mount, otherwise see instructions in [LAB-01](./LAB-01.md))

Copy everything to SD card:
```bash
# copy bootloader an kernel files
sudo cp ~/yocto-labs/build/tmp/deploy/images/zuehlkelabs/{MLO,u-boot.img,zImage} /media/$USER/boot
sudo cp ~/yocto-labs/build/tmp/deploy/images/zuehlkelabs/am335x-boneblack.dtb /media/$USER/boot/dtb

# overwrite the rootfs
sudo rm -rf /media/$USER/rootfs/**
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/zuehlkelabs/core-image-minimal-zuehlkelabs.tar.gz -C /media/$USER/rootfs
```

Next:
* sync and unmount the SD card
* place the SD card back into BBB
* boot the BBB from the SD card again

After booting up the BBB, you should see "zuehlkelabs login" as a confirmation that the new image has booted. Also, the hostname should then be "zuehlkelabs" as well:
```
Poky (Yocto Project Reference Distro) 3.1.4 zuehlkelabs /dev/ttyS0

zuehlkelabs login: root
root@zuehlkelabs:~# 
```
