#############################
# Base stage for all builds #
#############################
FROM alpine:3.13 as build_env

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


##################
# Build apriltag #
##################
FROM build_env as apriltag_build
ENV AP_VERSION=3.1.4

WORKDIR /usr/src
RUN curl https://codeload.github.com/AprilRobotics/apriltag/tar.gz/v$AP_VERSION -o apriltag.tar.gz \
    && tar -xzf apriltag.tar.gz \
    && cd /usr/src/apriltag-$AP_VERSION \
    && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=/opt/apriltag/$AP_VERSION -DCMAKE_BUILD_TYPE=Release ../ \
    && make -j4 all install \
    && cd /opt/apriltag/ && ln -s $AP_VERSION /opt/apriltag/current \
    && true


####################
# Minimal apriltag #
####################
FROM alpine:3.13 as apriltag
COPY --from=apriltag_build /opt/apriltag /opt/apriltag
# Add the libraries to "ldconfig"
RUN echo "/lib:/usr/local/lib:/usr/lib" >>/etc/ld-musl-$(uname -m).path \
    && echo "/opt/apriltag/current/lib64" >>/etc/ld-musl-$(uname -m).path \
    && true


######################
# Build librealsense #
######################
FROM build_env as librealsense_build

ENV RS_VERSION=2.42.0

COPY --from=apriltag /opt/apriltag /opt/apriltag

# Download and unpack (ordered like this so we can cache this phase when adjusting build settings / deps)
WORKDIR /usr/src
RUN curl https://codeload.github.com/IntelRealSense/librealsense/tar.gz/v$RS_VERSION -o librealsense.tar.gz \
    && tar -xzf librealsense.tar.gz \
    && true

# build deps
RUN apk --no-cache add \
    libpthread-stubs \
    linux-headers \
    musl-dev \
    libffi-dev \
    libbsd-dev \
    openssl-dev \
    libusb-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    glfw-dev \
    glm-dev \
    glew-dev \
    libxcb-dev \
    libxi-dev \
    fts-dev \
    libc-dev \
    hidapi-dev \
    vulkan-loader-dev \
    eudev-dev \
    && true

# Compile
# either alpine or librealsense is being weird with limits.h so MAX_INPUT is defined manually
# We also need to add a missing include to endian.h and sys/select.h
# and do a bit of other patching (like machine string, threads to main CMakeLists because aarch64 fails otherwise)
RUN cd /usr/src/librealsense-$RS_VERSION \
    && grep -q '#include <endian.h>' src/tm2/tm-device.cpp || sed -i '1s/^/#include <endian.h>\n/' src/tm2/tm-device.cpp \
    && grep -q '#include <sys/select.h>' tools/terminal/auto-complete.cpp || sed -i '1s/^/#include <sys\/select.h>\n/' tools/terminal/auto-complete.cpp \
    && sed -i 's/project(librealsense2 LANGUAGES CXX C)/project(librealsense2 LANGUAGES CXX C)\nfind_package(Threads REQUIRED)/' CMakeLists.txt \
    && sed -i 's/aarch64-linux-gnu/aarch64-alpine-linux-musl/' CMake/unix_config.cmake \
    && mkdir build && cd build \
    && cmake -DCMAKE_C_FLAGS="-D_BSD_SOURCE -D_GNU_SOURCE -Wno-pedantic -DMAX_INPUT=255" \
             -DCMAKE_CXX_FLAGS="-D_BSD_SOURCE -D_GNU_SOURCE -Wno-pedantic -DMAX_INPUT=255" \
             -DCMAKE_PREFIX_PATH=/opt/apriltag/current/ \
             -DCMAKE_INSTALL_PREFIX=/opt/librealsense/$RS_VERSION \
             -DBUILD_GRAPHICAL_EXAMPLES=OFF \
             -DFORCE_RSUSB_BACKEND=ON \
             -DCMAKE_BUILD_TYPE=Release ../ \
    && make -j4 all install \
    && cd /opt/librealsense/ && ln -s $RS_VERSION /opt/librealsense/current \
    && echo "/lib:/usr/local/lib:/usr/lib" >>/etc/ld-musl-$(uname -m).path \
    && echo "/opt/apriltag/current/lib64" >>/etc/ld-musl-$(uname -m).path \
    && echo "/opt/librealsense/current/lib64" >>/etc/ld-musl-$(uname -m).path \
    && true

# Move debug symbols to separate directory
RUN  for objfile in $(find /opt/ -type f -name '*.so*' -or -name '*.a*'); do \
       dbgfile=$(echo "$objfile" | awk -F/ '{OFS=FS}{$3=$3"-dbg";print $0".dbg"}') ; \
       mkdir -p $(dirname "$dbgfile") ; \
       objcopy --only-keep-debug "$objfile" "$dbgfile" ; \
       strip "$objfile" ; \
       objcopy --add-gnu-debuglink="$dbgfile" "$objfile" ; \
     done \
     && true


########################
# Minimal librealsense #
########################
FROM alpine:3.13 as librealsense

# Runtime deps
RUN apk --no-cache add \
    libusb \
    udev \
    libstdc++ \
    && true

COPY --from=apriltag /opt/apriltag /opt/apriltag
COPY --from=librealsense_build /opt/librealsense /opt/librealsense

# Add the libraries to "ldconfig"
RUN echo "/lib:/usr/local/lib:/usr/lib" >>/etc/ld-musl-$(uname -m).path \
    && echo "/opt/apriltag/current/lib64" >>/etc/ld-musl-$(uname -m).path \
    && echo "/opt/librealsense/current/lib64" >>/etc/ld-musl-$(uname -m).path \
    && true
WORKDIR /opt/librealsense/current/


##########################
# Debugging librealsense #
##########################
FROM librealsense as librealsense-dbg
COPY --from=librealsense_build /opt/librealsense-dbg /opt/librealsense-dbg
COPY --from=librealsense_build /opt/apriltag-dbg /opt/apriltag-dbg
