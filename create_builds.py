#!/usr/bin/env python3
"""Create manifest commands"""
import os
import sys
import subprocess
import itertools

from create_manifests import BUILDS, TAGS, ARCHS

if __name__ == "__main__":
    reponame = os.environ.get("DHUBREPO")
    if not reponame:
        print("Define DHUBREPO")
        sys.exit(1)
    archname = os.environ.get("IMGARCH")
    if not archname:
        print("Define IMGARCH")
        if archname not in ARCHS:
            print("IMGARCH must be one of {}".format(ARCHS))
        sys.exit(1)
    build_commands = []
    push_commands = [["docker", "login"]]
    for build in BUILDS:
        buildcmd = ["docker", "build", "--target", build]
        for tag in TAGS:
            tagstr = "{build}:{arch}-{tag}".format(arch=archname, tag=tag, build=build)
            repotag = reponame + "/" + tagstr
            buildcmd += ["-t", tagstr, "-t", repotag]
            push_commands.append(["docker", "push", repotag])
        buildcmd.append(".")
        build_commands.append(buildcmd)

    if os.environ.get("AUTORUN"):
        for cmd in itertools.chain(build_commands, push_commands):
            subprocess.run(" ".join(cmd), check=True, shell=True)
    else:
        print("** Run the following commands:")
        for cmd in itertools.chain(build_commands, push_commands):
            print(" ".join(cmd))
