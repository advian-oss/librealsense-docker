#!/usr/bin/env python3
"""Create buildx commands"""
import os
import sys

LATEST_RS = "2.42.0"
PLATFORMS = ["linux/amd64", "linux/arm64"]
TARGETS = ["librealsense", "librealsense-dbg"]
VARIANTS = ["alpine-3.13"]
RS_VERSIONS = [LATEST_RS]  # More library versions can be built if desired, just add the versions here


if __name__ == "__main__":
    reponame = os.environ.get("DHUBREPO")
    if not reponame:
        print("Define DHUBREPO")
        sys.exit(1)

    distros = [variant.split("-")[0] for variant in VARIANTS]

    hcl_targets = ""
    for target in TARGETS:
        for rsversion in RS_VERSIONS:
            latestag = ""
            if rsversion == LATEST_RS:
                latestag = f""", "{reponame}/{target}:latest" """
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
    tags = ["{reponame}/{target}:{rsversion}", "{reponame}/{target}:{rsversion}-{distro}", "{reponame}/{target}:{rsversion}-{distro}-{distroversion}"{latestag}]
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
