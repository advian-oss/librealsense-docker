# librealsense-docker

Dockerfile for compiling librealsense on Alpine.

## Build librealsense image itself

    docker build --target librealsense -t librealsense:latest -t librealsense:2.34.0 -t librealsense:2.34.0-alpine -t librealsense:2.34.0-alpine-3.11 .

## Add repo tags

    export DHUBREPO=myuser
    docker build --target librealsense -t $DHUBREPO/librealsense:latest -t $DHUBREPO/librealsense:2.34.0 -t $DHUBREPO/librealsense:2.34.0-alpine -t $DHUBREPO/librealsense:2.34.0-alpine-3.11 .

### Push to repo

    docker login
    docker push $DHUBREPO/librealsense:latest
    docker push $DHUBREPO/librealsense:2.34.0
    docker push $DHUBREPO/librealsense:2.34.0-alpine
    docker push $DHUBREPO/librealsense:2.34.0-alpine-3.11