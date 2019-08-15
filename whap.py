#!/usr/bin/python3

import os.path, sys, argparse
from importlib import import_module
from config import Get_chosen_plugins, Choose_plugins

# usage: whap.py [-f] <file>   - print the package name that owns <file>
# usage: whap.py -i <file> - print info about the package that owns <file>
# usage: what.py -l <file> - print all the files in the package that owns <file>
# the -f is ignored, but provides compatibility with rpm
parser = argparse.ArgumentParser(description="WHAt Package?")
normal = parser.add_argument_group()
normal.add_argument('-f','--file', action='store_true')
normal.add_argument('-i','--info', action='store_true')
normal.add_argument('-l','--list', action='store_true')
normal.add_argument('file_full_path', nargs='?', default=None)

conf = parser.add_argument_group()
conf.add_argument('-c', '--config', action='store_true')

args = parser.parse_args()

if (args.config):
   Choose_plugins()
   # Choose_plugins exits the program

if (args.file_full_path is None):
   print("You must specify a file to check")
   exit(1)

if (not os.path.exists(args.file_full_path)):
   print("File",args.file_full_path,"does not exist (or you cannot see it with your permissions)")
   exit(1)

plugins = Get_chosen_plugins()

if (len(plugins) == 0):
   print("Your configuration has no plugins.  Run ", __file__, "-c to change your configuration")
   exit(1)

# first we have to figure out if any packages match
packages = []
for plugin in plugins.keys():
   module_name = plugins[plugin]
   #print ('Trying', plugin, 'module', module_name)
   try:
      mod = import_module(module_name)
   except:
      print("...failed")
      continued

   Find = getattr(mod, "Find")
   if (Find):
      packages = Find(args.file_full_path)
      for package in packages:
         print("   ", package)
         if (args.info):
            Info = getattr(mod, "Info")
            if (Info):
               print()
               print(Info(package))
         if (args.list):
            Files = getattr(mod, "Files")
            if (Files):
               print()
               print('\n'.join(Files(package)))



