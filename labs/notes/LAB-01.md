
# Lab 1: First Yocto Project build

## Lab 1 - Lab Setup

Setup the `~/yocto-labs/` playground:
```bash
# start from user home
cd $HOME

# copy labs
cp /vagrant/labs/content/yocto-labs.tar.gz .
tar xzvf yocto-labs.tar.gz

# get additional layers and checkout the dunfell branch
cd yocto-labs
git clone git://git.yoctoproject.org/poky.git --branch dunfell
git clone git://git.yoctoproject.org/meta-ti.git --branch dunfell
git clone git://git.yoctoproject.org/meta-arm.git --branch dunfell
```

Initialize the build directory under `~/yocto-labs/build`:
```bash
cd ~/yocto-labs
source poky/oe-init-build-env
```

Configure the layers and adapt the config for "beaglebone":
```bash
# add the meta-ti and meta-arm layers 
bitbake-layers add-layer ../meta-ti ../meta-arm/meta-arm ../meta-arm/meta-arm-toolchain

# remove the meta-yocto-bsp layer which conflicts with meta-ti
bitbake-layers remove-layer ../poky/meta-yocto-bsp

# set MACHINE type to beaglebone and don't waste disk space
echo 'MACHINE = "beaglebone"' >> conf/local.conf
echo 'INHERIT += "rm_work"' >> conf/local.conf
```

## Lab 1 - Build the Image

Again, make sure you have the environment set up:
```bash
cd ~/yocto-labs
source poky/oe-init-build-env
```

Now you can build the "core-image-minimal" image (might take a while...):
```bash
bitbake core-image-minimal
```

The output should look similar to this:
```bash
$ bitbake core-image-minimal
Parsing recipes: 100% |###########################################################| Time: 0:00:14
Parsing of 1050 .bb files complete (0 cached, 1050 parsed). 1639 targets, 206 skipped, 0 masked, 0 errors.
NOTE: Resolving any missing task queue dependencies

Build Configuration:
BB_VERSION           = "1.46.0"
BUILD_SYS            = "x86_64-linux"
NATIVELSBSTRING      = "universal"
TARGET_SYS           = "arm-poky-linux-gnueabi"
MACHINE              = "beaglebone"
DISTRO               = "poky"
DISTRO_VERSION       = "3.1.4"
TUNE_FEATURES        = "arm armv7a vfp thumb neon callconvention-hard"
TARGET_FPU           = "hard"
meta                 
meta-poky            = "dunfell:75997e9e80d8835b2b0bbfd6d223892cd47fb4ee"
meta-ti              = "dunfell:efabc3ccceec3d6e65f7fae5e15bec763c1078ea"
meta-arm             
meta-arm-toolchain   = "dunfell:c4f04f3fb66f8f4365b08b553af8206372e90a63"

Initialising tasks: 100% |########################################################| Time: 0:00:02
Sstate summary: Wanted 226 Found 226 Missed 0 Current 939 (100% match, 100% complete)
NOTE: Executing Tasks
NOTE: Tasks Summary: Attempted 3620 tasks of which 3370 didn't need to be rerun and all succeeded.
```

Once this succeeded without errors, you are ready write the outputs (bootloader files and rootfs) to the SD card.

## Lab 1 - Prepare SD Card

We need to prepare the SD card first. It should come up as `/dev/sdc` within the developer VM.

Unmount SD card (in case it is mounted):
```bash
sudo umount /dev/sdc1
sudo umount /dev/sdc2
```

Format the SD card:
```bash
sudo ~/yocto-labs/zuehlke-lab-data/script/format_sdcard.sh /dev/sdc
```

Setup mount points and mount the SD card (boot and rootfs partitions):
```bash
sudo mkdir -p /media/$USER/{boot,rootfs}
sudo mount /dev/sdc1 /media/$USER/boot
sudo mount /dev/sdc2 /media/$USER/rootfs
```

Copy bootloader files to the boot partition:
```bash
sudo cp ~/yocto-labs/build/tmp/deploy/images/beaglebone/{MLO,u-boot.img,zImage} /media/$USER/boot
sudo cp ~/yocto-labs/build/tmp/deploy/images/beaglebone/am335x-boneblack.dtb /media/$USER/boot/dtb
```

Uncompress the filesystem to the rootfs partition:
```bash
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/beaglebone/core-image-minimal-beaglebone.tar.xz -C /media/$USER/rootfs
sudo sync
```

Don't forget to unmount the SD card when you are done:
```bash
sudo umount /dev/sdc1
sudo umount /dev/sdc2
```

Next:
 * wire the USB-serial adapter with the BBB **while BBB is powered off** (see labs for details!)
 * connect the USB-serial adapter and pass it to the VM

Open Serial port:
```bash
picocom -b 115200 /dev/ttyUSB0
```

Next:
 * remove the SD card from the reader and insert it into the BBB
 * in order to boot from the SD card:
   * power off the BBB (unplug power)
   * press the button next to the SD card while powering on the BBB
   * review serial output and ensure it's UBoot 2020 (i.e. from the sd card)
   * interrupt the boot process to drop into uboot

Once you successfully dropped into uboot, configure boot commands (needs to be done only once after reformatting):
```bash
setenv bootcmd 'mmc rescan; fatload mmc 0 0x80200000 zImage; fatload mmc 0 0x82000000 dtb; bootz 0x80200000 - 0x82000000'
setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait rw'
saveenv
```

Login:
 * you can log in with "root" (no password)

Further notes:
 * Indicators on whether it booted from SD card or internal memory
    - UBoot 2016 -> factory uboot
    - UBoot 2020 -> our poky uboot
 * what to change when?
    - kernel changes -> zImage
    - otherwise -> rootfs
