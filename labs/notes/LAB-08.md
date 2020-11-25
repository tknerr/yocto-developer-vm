# Yocto Training Notes 2020-11-25

## Lab 8 - Create an App Development SDK for our Image

Creating an SDK (inlcudes cross-compilers, linkers, library headers, etc) allows application developers to develop apps for our specific image. It can be built via Yocto and distributed to developers, so they can develop / cross-compile for the target without the need for having Yocto installed.

Generate the SDK for our "zuehlkelabs-image-minimal" image like so (might take a while):
```bash
bitbake -c populate_sdk zuehlkelabs-image-minimal
```

Once completed, you should find the generated SDK in `~/yocto-labs/build/tmp/deploy/sdk/`

Running `ls -lah ~/yocto-labs/build/tmp/deploy/sdk/` should give you similar output:
```
-rw-r--r-- 2 user user      8857 Nov 25 12:25 poky-glibc-x86_64-zuehlkelabs-image-minimal-cortexa8t2hf-neon-zuehlkelabs-toolchain-3.1.4.host.manifest
-rwxr-xr-x 2 user user 132064884 Nov 25 12:28 poky-glibc-x86_64-zuehlkelabs-image-minimal-cortexa8t2hf-neon-zuehlkelabs-toolchain-3.1.4.sh*
-rw-r--r-- 2 user user     21226 Nov 25 12:24 poky-glibc-x86_64-zuehlkelabs-image-minimal-cortexa8t2hf-neon-zuehlkelabs-toolchain-3.1.4.target.manifest
-rw-r--r-- 2 user user    243461 Nov 25 12:24 poky-glibc-x86_64-zuehlkelabs-image-minimal-cortexa8t2hf-neon-zuehlkelabs-toolchain-3.1.4.testdata.json
```

## Lab 8 - Install the SDK

In order to install the SDK, just run the generated .sh script (it's quite big and contains all the contents).

It will prompt you for the install location, where you can enter the install location (e.g. `~/yocto-labs/sdk/`):
```
user@yocto-dev-vm:~/yocto-labs/build$ tmp/deploy/sdk/poky-glibc-x86_64-zuehlkelabs-image-minimal-cortexa8t2hf-neon-zuehlkelabs-toolchain-3.1.4.sh 
Poky (Yocto Project Reference Distro) SDK installer version 3.1.4
=================================================================
Enter target directory for SDK (default: /opt/poky/3.1.4): ~/yocto-labs/sdk
You are about to install the SDK to "/home/user/yocto-labs/sdk". Proceed [Y/n]? Y
Extracting SDK..............................................done
Setting it up...done
SDK has been successfully set up and is ready to be used.
Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.
 $ . /home/user/yocto-labs/sdk/environment-setup-cortexa8t2hf-neon-poky-linux-gnueabi
```

## Lab 8 - Cross-compile Ctris with the SDK

Download and unpack the ctris sources:
```
mkdir ~/yocto-labs/sdk/ctris
cd ~/yocto-labs/sdk/ctris
wget  https://download.mobatek.net/sources/ctris-0.42-1-src.tar.bz2
tar xvf ctris-0.42-1-src.tar.bz2
tar xvf ctris-0.42.tar.bz2
cd ctris-0.42
```

Source the SDK environment and compile it with the tools included in the SDK:
```
source ~/yocto-labs/sdk/environment-setup-cortexa8t2hf-neon-poky-linux-gnueabi
make
```

Verify that is has been compiled for as an ELF 32-bit ARM executable (use the `file` command):
```
user@yocto-dev-vm:~/yocto-labs/sdk/ctris/ctris-0.42$ file ctris
ctris: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, BuildID[sha1]=dbe8ceddb6864eaf394754953eaf7d67bee30014, for GNU/Linux 3.2.0, with debug_info, not stripped
```

## Lab 8 - Configure Networking between BBB and VM

**NOTE:** this is a short digression from the actual Lab 8, as I didn't set up networking in Lab 2

Below are the steps that need to be done manually in order to configure networking on the BBB.
It would be much better to do this via a dedicated recipe that a) installs dropbear and b) configures the static IP.

### Configure Network on BBB

Configure static IP "192.168.0.100" on BBB via `vi /etc/network/interfaces` and add/edit:
```
# Wired or wireless interfaces
auto eth0
iface eth0 inet static
        address 192.168.0.100
        netmask 255.255.255.0
```

After changing the network config, reload the configuration:
```bash
ifdown eth0
ifup eth0
```

### Configure Network in VM

Configure IP address "192.168.0.1" on "eth1" in the VM and bring it up:
```
sudo ip addr add 192.168.0.1/24 dev eth1
sudo ip link set eth1 up
```

Check if you can ping the BBB from the VM:
```
ping 192.168.0.100
```

### Install Dropbear SSH server

Also make sure to include dropbear in the image, e.g. in `~/yocto-labs/build/conf/local.conf`:
```
...
IMAGE_INSTALL_append = " dropbear"
...
```

(and don't forget to rebuild the image)


## Lab 8 - Upload Ctris to BBB and run it!

Finally, once you have a dropbear SSH server running on BBB, you can upload and play ctris!

Upload via SCP:
```bash
scp ctris root@192.168.0.100:/usr/bin/ctris
```

Login and play:
```
ssh root@192.168.0.100
ctris
```
