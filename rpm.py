#!/usr/bin/python
# coding: interpy

from __future__ import print_function

import argparse
import interpy
import os
import subprocess
import sys

from hs_jenkins import time_taken

def abort(message):
    print(message)
    sys.exit(1)

def merge_spec(spec_file):
    spec_cmd = "git checkout --merge remotes/origin/spec #{spec_file}"

    time_taken(spec_cmd)

def build_tarball(tar_prefix, tarball):
    tarball_cmd = "git archive --format=tar.gz --prefix=#{tar_prefix} HEAD > #{tarball}"

    time_taken(tarball_cmd)

def build_cleanup(spec_file, tarball):
    git_reset_spec = "git reset #{spec_file}"

    time_taken(git_reset_spec)

    rm_spec = "rm #{spec_file}"

    time_taken(rm_spec)

    rm_tarball = "rm #{tarball}"

    time_taken(rm_tarball)

    rm_dirs = 'rm -rf BUILD BUILDROOT RPMS SPECS SRPMS'

    time_taken(rm_dirs)

def build_compile(spec_file):
    compile = "rpmbuild --define '_topdir '$PWD --define '_sourcedir '$PWD -bb #{spec_file}"

    time_taken(compile)

def find_version(spec_file):
    with open(spec_file) as origin_file:
        for line in origin_file:
            if line.startswith('Version:'):
                version = line.strip().split()[1]
    return version

def build_rpm(spec_file, tar_prefix, tarball):
    build_tarball(tar_prefix, tarball)
    build_compile(spec_file)

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='name', help='repo name', required=True)
parser.add_argument('-c', action='store_true', default=False, dest='cleanup', help='cleanup will be done')
parser.add_argument('-t', action='store_true', default=False, dest='thirdparty', help='third party repo')

args = parser.parse_args()

cleanup = args.cleanup
name = args.name
src_dir = "../#{name}"

print("Changing directory to #{src_dir}")
os.chdir(src_dir)

spec_file = "#{name}.spec"
if thirdparty:
  merge_spec(spec_file)
version = find_version(spec_file)
tar_dir = "#{name}-#{version}"
tar_prefix = "#{tar_dir}/"
tarball = "#{name}-#{version}.tar.gz"

if cleanup:
    build_cleanup(spec_file, tarball)
else:
    build_rpm(spec_file, tar_prefix, tarball)
