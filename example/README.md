# rs-reset

Very simple C++ example application to ask all connected realsense devices to reset

Used as an example on how to use the minimal librealsense Docker base image.

## Usage

    docker build --target myapp -t myapp:latest .
    sudo docker run --privileged -it myapp:latest
