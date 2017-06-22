# coding: interpy

from __future__ import print_function

import interpy

from timeit import timeit

def time_taken(cmd):
    print("Running #{cmd}")
    time = timeit(stmt="run_cmd(\"#{cmd}\")", setup="from run_cmd import run_cmd", number=1)
    print("#{cmd}: #{time}s")
