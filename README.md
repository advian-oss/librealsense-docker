# librealsense-docker

Dockerfile for compiling librealsense on Alpine.

## Using

See the `example` directory.

## Building images

### Enable `buildx`

On x86 Linux, the following _may_ be necessary to install `buildx`:

    export DOCKER_BUILDKIT=1
    docker build --platform=local -o . git://github.com/docker/buildx
    mkdir -p ~/.docker/cli-plugins
    mv buildx ~/.docker/cli-plugins/docker-buildx

### Enable `docker/binfmt`

In order to be able to build images for foreign architectures, the `docker/binfmt`
image should pulled and run. This will make [`qemu-user-static`](https://github.com/multiarch/qemu-user-static)
available on the host:

    docker run --rm --privileged docker/binfmt:a7996909642ee92942dcd6cff44b9b95f08dad64  # latest as of 2020-10-20

### Create a "builder" instance

    docker buildx create --name librealsensebuilder
    docker buildx use librealsensebuilder
    docker buildx inspect --bootstrap

### Build and push

    export DHUBREPO=myrepo
    ./create_builds.py librealsense > librealsense.hcl
    ./create_builds.py librealsense-dbg > librealsense-dbg.hcl
    docker login
    docker buildx bake --push --file ./librealsense.hcl
    docker buildx bake --push --file ./librealsense-dbg.hcl

The `create_builds.py` script output includes the Docker commands above as HCL file comments.
