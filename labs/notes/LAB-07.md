# Lab 7: Create a custom image

## Lab 7 - Create a Custom Image

So far we used the "core-image-minimal" image, which defines what gets installed into the rootfs.
By defining our own custom "zuehlkelabs-image-minimal" we can get more control over that.

Review the existing "core-image" class and "core-image-minimal" recipe:
 * `poky/meta/classes/core-image.bbclass` - a class that you can inherit from 
 * `poky/meta/recipes-core/core-image-minimal.bb` - a recipe that you can require

Let's create our custom image in `meta-zuehlkelabs/recipes-core/images/zuehlkelabs-image-minimal.bb`:
```
inherit core-image

DESCRIPTION = "Zuehlke Labs Custom Image"
IMAGE_INSTALL = "packagegroup-core-boot ninvaders ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_FSTYPES = "tar.bz2 cpio squashfs"
LICENSE = "MIT"
```

Next:
* shutdown BBB and remove SD card
* insert SD card into reader (it should auto-mount, otherwise see instructions in [LAB-01](./LAB-01.md))

Overwrite the rootfs with the newly created image:
```bash
# overwrite the rootfs
sudo rm -rf /media/$USER/rootfs/**
sudo tar xpf ~/yocto-labs/build/tmp/deploy/images/zuehlkelabs/zuehlkelabs-image-minimal-zuehlkelabs.tar.gz -C /media/$USER/rootfs
```

Next:
* sync and unmount the SD card
* place the SD card back into BBB
* boot the BBB from the SD card again

Final check: see if it boots and has nInvaders installed


## Lab 7 - Create our own Package Group

Adding a packagegroup is a means to group several packages / recipes togehter.

Review:
* Look for existing package groups via `find ~/yocto-labs/ -name packagegroups`

Lets create our own "zuehlelabs-games" packagegroup in `meta-zuehlkelabs/recipes-games/packagegroups/packagegroup-zuehlkelabs-games`:
```
inherit packagegroup

SUMMARY = "Collection of custom games"
DESCRIPTION = "Collection of custom games to be added as a packagegroup"

RDEPENDS_${PN} = "\
    ninvaders \
    "
```

Also make sure to reference it in our `zuehlkelabs-image-minimal.bb` image definition:
```
...
IMAGE_INSTALL = "packagegroup-core-boot packagegroup-zuehlke-games ${CORE_IMAGE_EXTRA_INSTALL}"
...
```

## Lab 7 - Create a Debug Image Variant

By adding the IMAGE_FEATURE "dbg-pkgs" the debug symbols for all the executables will be installed inside image, so they can be debugged within the image. Note: it **does not** install debugging tools like gdb, strace, etc -- these need to be installed separately (via IMAGE_INSTALL variable) if you need them.

So let's add a new `zuehlkelabs-image-minimal-dbg.bb` image definition in `meta-zuehlkelabs/recipes-core/images/`:
```
require recipes-core/images/zuehlkelabs-image-minimal.bb

DESCRIPTION = "Zuehlke Labs Custom Image (Debug)"

# keep debug symbols wihtin image
IMAGE_FEATURES += "dbg-pkgs"

# install additional debugging tools
IMAGE_INSTALL += "gdb strace"
```

You can the bake the debug image: `bitbake zuehlkelabs-image-minimal-dbg`

Finally, to verify:
* check that `/usr/bin/.debug/nInvaders` is present
* check size of `du -hs /usr/bin/.debug/` which should be roughly 10M
* check for presence of `gdb` and `strace` tools
