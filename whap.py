#!/usr/bin/python3

import os, argparse
from importlib import import_module
from functools import lru_cache

from config import Get_chosen_plugins, Choose_plugins          # in this directory

@lru_cache(maxsize=1)         # only execute this once, then return same value whenever it is later called
def getArgs():
    # usage: whap.py [-f] <file>   - print the package name that owns <file>
    # usage: whap.py -i <file> - print info about the package that owns <file>
    # usage: what.py -l <file> - print all the files in the package that owns <file>
    # the -f is ignored, but provides compatibility with rpm
    parser = argparse.ArgumentParser(description="WHAt Package?")
    parser.add_argument('-f','--file', action='store_true')
    parser.add_argument('-i','--info', action='store_true')
    parser.add_argument('-l','--list', action='store_true')
    parser.add_argument('-c', '--config', action='store_true')
    parser.add_argument('file_full_path', nargs='?', default=None)    # required for all commands except --config

    args = parser.parse_args()         # exits program if it doesn't like command line
    validateArgs(args)
    return args

def validateArgs(args):
    if (not args.config):
        # for all other commands file_full_path is required
        if (not args.file_full_path):
            print("You must specify a file to check")
            exit(1)

        if (not os.path.exists(args.file_full_path)):
            print("File",args.file_full_path,"does not exist (or you cannot see it with your permissions)")
            exit(1)

def executePlugin(plugin, args):
    mod = importPlugin(plugin)
    if (mod is False): return

    callable = findCallable(mod, plugin)
    if (callable is False): return

    callable(args)

def importPlugin(plugin):
    # plugin is a pair (informal name, python module name)
    try:
        mod = import_module(plugin[1])
        return mod
    except:
        print("Failed to import plugin", plugin[0])
        return False

def findCallable(mod, plugin):
    try:
        callable = getattr(mod, 'executePlugin')
        return callable
    except AttributeError:
        print("Plugin module", plugin[1], "has the wrong format")
        return False




# "main" begins here

args = getArgs()

if (args.config):              # this command is handled separately
    Choose_plugins()
    exit(0)

plugins = Get_chosen_plugins()
if (not plugins):
    print("Your configuration has no plugins.  Run ", __file__, "-c to change your configuration")
    exit(1)

# now handle all non-config commands
[executePlugin(plugin, args) for plugin in Get_chosen_plugins()]

