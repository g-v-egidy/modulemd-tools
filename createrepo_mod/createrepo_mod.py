#!/usr/bin/python3

"""
A small wrapper around `createrepo_c` and `modifyrepo_c` to provide an easy tool
for generating module repositories.

This is supposed to be only a temporary solution, in the future we would like to
have the modularity support implemented in `createrepo_c` itself. See

https://bugzilla.redhat.com/show_bug.cgi?id=1816753

Please see the official Fedora Modularity documentation for the reference of how
module repositories should be created

https://docs.fedoraproject.org/en-US/modularity/hosting-modules/
"""


import os
import sys
import subprocess
import argparse


def run_createrepo(args):
    cmd = ["createrepo_c"] + args
    proc = subprocess.run(cmd, check=True)
    return proc.returncode


def run_modifyrepo(path, compress_type=None):
    cmd = [
        "modifyrepo_c",
        "--mdtype", "modules",
        os.path.join(path, "modules.yaml"),
        os.path.join(path, "repodata"),
    ]

    if compress_type:
        cmd.extend(["--compress-type", compress_type])

    proc = subprocess.run(cmd, check=True)
    return proc.returncode


def main():
    run_createrepo(sys.argv[1:])
    parser = get_arg_parser()
    args, _ = parser.parse_known_args()
    run_modifyrepo(args.path, "gz")


def get_arg_parser():
    # We are not going to define the whole parser here. Instead, we want to
    # pass all the input parameters to `createrepo_c` and let it handle them.
    #
    # We only need to define parser for a small subset of parameters that we
    # need to work within this script.

    description = ("A small wrapper around createrepo_c and modifyrepo_c to"
                   "provide an easy tool for generating module repositories")
    parser = argparse.ArgumentParser("%prog", description=description)
    parser.add_argument("path", metavar="directory_to_index",
                        help="Directory to index")
    return parser


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as ex:
        sys.stderr.write("Error: {0}\n".format(str(ex)))
        sys.exit(1)
