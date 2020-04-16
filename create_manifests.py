#!/usr/bin/env python3
"""Create manifest commands"""
import os
import sys
import subprocess

ARCHS = ["x86_64", "aarch64"]
TAGS = ["latest", "2.34.0", "2.34.0-alpine", "2.34.0-alpine-3.11"]
BUILDS = ["librealsense", "librealsense-dbg"]


if __name__ == "__main__":
    reponame = os.environ.get("DHUBREPO")
    if not reponame:
        print("Define DHUBREPO")
        sys.exit(1)
    tag_commands = []
    inspect_commands = []
    push_commands = [["docker", "login"]]
    for build in BUILDS:
        for tag in TAGS:
            manifestag = "{repo}/{build}:{tag}".format(
                repo=reponame, tag=tag, build=build
            )
            cmd = ["docker", "manifest", "create", "--amend", manifestag]
            for arch in ARCHS:
                cmd.append(
                    "{repo}/{build}:{arch}-{tag}".format(
                        repo=reponame, arch=arch, tag=tag, build=build
                    )
                )
            tag_commands.append(cmd)
            inspect_commands.append("docker manifest inspect {}".format(manifestag))
            push_commands.append(["docker", "manifest", "push", manifestag])

    if os.environ.get("AUTORUN"):
        for cmd in tag_commands:
            subprocess.run(cmd, check=True, shell=True)
        for cmd in push_commands:
            subprocess.run(cmd, check=True, shell=True)
    else:
        print("** Run the following commands:")
        for cmd in tag_commands:
            print(" ".join(cmd))

    print("** To check results run:")
    for cmd in inspect_commands:
        print(cmd)

    if not os.environ.get("AUTORUN"):
        print("** to push the manifests run:")
        for cmd in push_commands:
            print(" ".join(cmd))
