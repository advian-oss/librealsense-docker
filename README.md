# librealsense-docker

Dockerfile for compiling librealsense on Alpine.

## Using

See the `example` directory.

## Build librealsense image itself

    docker build --target librealsense -t librealsense:latest -t librealsense:2.34.0 -t librealsense:2.34.0-alpine -t librealsense:2.34.0-alpine-3.11 .

## Add repo tags

    export DHUBREPO=myuser
    export IMGARCH=`uname -m`
    docker build --target librealsense \
           -t $DHUBREPO/librealsense:$IMGARCH-latest \
           -t $DHUBREPO/librealsense:$IMGARCH-2.34.0 \
           -t $DHUBREPO/librealsense:$IMGARCH-2.34.0-alpine \
           -t $DHUBREPO/librealsense:$IMGARCH-2.34.0-alpine-3.11 \
           .

### Push to repo

    docker login
    docker push $DHUBREPO/librealsense:$IMGARCH-latest
    docker push $DHUBREPO/librealsense:$IMGARCH-2.34.0
    docker push $DHUBREPO/librealsense:$IMGARCH-2.34.0-alpine
    docker push $DHUBREPO/librealsense:$IMGARCH-2.34.0-alpine-3.11

### Create manifests

See <https://docs.docker.com/engine/reference/commandline/manifest/>

Then run `create_manifests.py` to get a list of commands and run them.
