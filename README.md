# librealsense-docker

Dockerfile for compiling librealsense on Alpine.

## Using

See the `example` directory.

## Docker hub

### Building

Run `crate_builds.py` to get list of commands to run to create and push all the tag variants.

    DHUBREPO=myrepo IMGARCH=`uname -m` ./crate_builds.py

### Multiarch manifests

See <https://docs.docker.com/engine/reference/commandline/manifest/>

Then run `create_manifests.py` to get a list of commands and run them.

    DHUBREPO=myrepo ./create_manifests.py
