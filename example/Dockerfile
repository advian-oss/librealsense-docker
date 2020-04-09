######################
# Base builder image #
######################
FROM eeroafheurlin/librealsense:2.34.0-alpine-3.11 as builder_base
# Very basic compiler deps
RUN apk --no-cache add \
    curl \
    gzip \
    tar \
    build-base \
    cmake \
    llvm \
    clang \
    && true


##########################
# Our specific build env #
##########################
FROM builder_base as builder
COPY . /usr/src/rs-reset
WORKDIR /usr/src/rs-reset
RUN mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=/opt/rs-reset -DCMAKE_BUILD_TYPE=Release ../ \
             -DCMAKE_PREFIX_PATH=/opt/librealsense/current \
    && make -j4 all \
    && true


#####################
# Minimal app image #
#####################
FROM eeroafheurlin/librealsense:2.34.0-alpine-3.11 as myapp
COPY --from=builder /usr/src/rs-reset/build/rs-reset /usr/local/bin

ENTRYPOINT [ "sh", "-c" ]
CMD ["/usr/local/bin/rs-reset"]
