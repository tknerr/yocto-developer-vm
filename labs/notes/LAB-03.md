
# Yocto Training Notes 2020-11-23

## Lab 3 - Creating a Custom Layer

Create the "meta-zuehlkelabs" layer with priority 7:
```bash
bitbake-layers create-layer --priority 7 ../meta-zuehlkelabs
```

Add the layer to `conf/local.conf`:
```bash
bitbake-layers add-layer ../meta-zuehlkelabs
```

Review layers:
```bash
bitbake-layers show-layers
```

Output should be similar to this:
```bash
$ bitbake-layers show-layers
NOTE: Starting bitbake server...
layer                 path                                      priority
==========================================================================
meta                  /home/user/yocto-labs/poky/meta           5
meta-poky             /home/user/yocto-labs/poky/meta-poky      5
meta-ti               /home/user/yocto-labs/meta-ti             6
meta-arm              /home/user/yocto-labs/meta-arm/meta-arm   6
meta-arm-toolchain    /home/user/yocto-labs/meta-arm/meta-arm-toolchain  30
meta-zuehlkelabs      /home/user/yocto-labs/meta-zuehlkelabs    7
```

