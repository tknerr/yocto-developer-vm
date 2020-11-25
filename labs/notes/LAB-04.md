
# Lab 4: Add a custom application

## Lab 4 - Overview

We will create a custom recipe to install the nInvaders game:

1. Create nInvaders Recipe
2. Bake the Image and run nInvaders on the BBB

## Lab 4 - Create nInvaders Recipe

* create recipe manually or when layer is created
* run `bitbake ninvaders` to bake only that
* run `bitbake -c clean ninvaders` clean it

Recipe name must be `meta-zuehlkelabs/recipes-games/ninvaders/ninvaders_0.1.1.bb`
 * follow the directory structure (-> convention)
 * use the upstream version for the recipe version (-> convention)

Add SRC_URL and SHA:
```
SRC_URI = "${SOURCEFORGE_MIRROR}/ninvaders/${PN}-${PV}.tar.gz"
```

It will complain about missing SHA, so let's add:
```
SRC_URI[sha256sum] = "bfbc5c378704d9cf5e7fed288dac88859149bee5ed0850175759d310b61fd30b"
```

License file:
 * you can find the extracted package in $BUILD_DIR/tmp/work/arm7.../ninvaders
 * find the `gpl.txt` there and run `md5sum gpl.txt` over it

Now you can add:
```
LIC_FILES_CHKSUM = "file://gpl.txt;md5=393a5ca445f6965873eca0259a17f833"
```

Next:
 * add the `do_compile` task (comes by default, but better be explicit)
 * add the `do_install` task (to install it to `/usr/bin/nInvaders`)
 * split into the version agnostic `ninvaders.inc` file and version-specific `ninvaders_0.1.1.bb` file

The resulting `meta-zuehlkelabs/recipes-games/ninvaders/ninvaders.inc` file should look similar to that:
```
SUMMARY = "NInvaders recipe"
DESCRIPTION = "Recipe to install the NInvaders application"
LICENSE = "MIT"

do_compile() {
    oe_runmake
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 nInvaders ${D}${bindir}
}
```

The resulting `meta-zuehlkelabs/recipes-games/ninvaders/ninvaders_0.1.1.bb` file should look similar to that:
```
require ninvaders.inc

# source URI and checksum for ninvaders source files
SRC_URI = "${SOURCEFORGE_MIRROR}/ninvaders/${BPN}-${PV}.tar.gz"
SRC_URI[sha256sum] = "bfbc5c378704d9cf5e7fed288dac88859149bee5ed0850175759d310b61fd30b"

# license file and checksum within the extracted source tarball
LIC_FILES_CHKSUM = "file://gpl.txt;md5=393a5ca445f6965873eca0259a17f833"

# ncurses is a build- and runtime dependency
DEPENDS = "ncurses"
RDEPENDS_${PV} = "ncurses"

# fix build issue to make make find the ncurses lib
EXTRA_OEMAKE = "-e"
```

You should be ready to build the "ninvaders" recipe now:
 * bake it using `bitbake ninvaders`
 * compile output in `~/yocto-labs/build/tmp/work/armv7at2hf-neon-poky-linux-gnueabi/ninvaders/0.1.1-r0` (?)
 * Hint: running `bitbake -c devshell ninvaders` brings you there with the environment properly set up


## Lab 4 - Bake the Image and run nInvaders on the BBB

Once the "ninvaders" recipe compiles successfully, we can integrate it into the beagleboard image.

First of all, we need to add it to the image:
 * in `build/conf/local.conf` add the "ninvaders" recipe via `IMAGE_INSTALL_append`

Then we can re-create the image:
 * `bitbake core-image-minimal`

Next:
* shutdown BBB and remove SD card
* insert SD card into reader (it should auto-mount, otherwise see instructions in [LAB-01](./LAB-01.md))

Update the rootfs on the SD card:
```bash
# overwrite the rootfs
sudo rm -rf /media/$USER/rootfs/**
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/beaglebone/core-image-minimal-beaglebone.tar.xz -C /media/$USER/rootfs
```

Next:
* sync and unmount the SD card
* place the SD card back into BBB
* boot the BBB from the SD card again

Once the BBB has booted, you should be able to log in as "root" and run `nInvaders` (hint: via serial console this is barely playable, game experience should be much better when connected via SSH ;-))