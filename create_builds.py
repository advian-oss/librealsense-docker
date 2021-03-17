#!/usr/bin/env python3
"""Create buildx commands"""
import os
import sys

PLATFORMS = ["linux/amd64", "linux/arm64"]
TARGETS = ["librealsense", "librealsense-dbg"]
VARIANTS = ["alpine-3.13"]
RS_VERSIONS = ["2.42.0"]


if __name__ == "__main__":
    reponame = os.environ.get("DHUBREPO")
    if not reponame:
        print("Define DHUBREPO")
        sys.exit(1)

    if len(sys.argv) != 2 or not sys.argv[1] in TARGETS:
        print(f"""Specify target, one of: {", ".join(TARGETS)}""")
        sys.exit(1)
    target = sys.argv[1]
    distros = [variant.split("-")[0] for variant in VARIANTS]

    hcl_targets = ""
    for rsversion in RS_VERSIONS:
        for variant in VARIANTS:
            distro, distroversion = variant.split("-")
            dockerfile = f"Dockerfile_{distro}"
            hcl_targets += f"""
target "{target}:{distro}" {{
    dockerfile = "{dockerfile}"
    platforms = [{", ".join(f'"{platform}"' for platform in PLATFORMS)}]
    target = "{target}"
    args = {{
        RS_VERSION = "{rsversion}"
    }}
    tags = ["{reponame}/{target}:{rsversion}", "{reponame}/{target}:{rsversion}-{distro}", "{reponame}/{target}:{rsversion}-{distro}-{distroversion}"]
}}
"""

    print(f"""
// To build and push images, redirect this output to a file named "{target}.hcl" and run:
//
// docker login
// docker buildx bake --push --file ./{target}.hcl

group "default" {{
    targets = [{", ".join(f'"{target}:{distro}"' for distro in distros)}]
}}""")
    print(hcl_targets)
