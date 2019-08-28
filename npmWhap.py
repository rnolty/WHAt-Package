# whap plugin for NPM

# as far as I can see, NPM doesn't have any facility for listing files
#    in a package, but the structure on disk makes it easy -- just
#    look for a package.json file in the directory hierarchy

import os, os.path, json
from functools import lru_cache


def executePlugin(args):
    # args was created by argparse, but more importantly it has boolean attributes 'info' and 'list'
    print("Trying npm:")
    (packages,path) = _find(args.file_full_path)         # packages is list with either 0 or 1 element
    [_info(path) for package in packages if args.info]
    [_files(path) for package in packages if args.list]

@lru_cache(maxsize=1)
def _getJSONData(path):
    with open(path) as pkgFile:
        return json.load(pkgFile)
    
@lru_cache(maxsize=100)
def _checkDir(dir_):
    if (dir_ == '/'): return None                                            # we have exhausted ancestors
    if (os.path.exists(os.path.join(dir_, 'package.json'))): return dir_     # this is the package directory
    return _checkDir(os.path.split(dir_)[0])                                 # check parent

def _find(fileFullPath):
    pkgDir = _checkDir(os.path.dirname(fileFullPath))                        # find ancestor with a package.json
    if (pkgDir is None): return [[],None]
    configs = _getJSONData(os.path.join(pkgDir, 'package.json'))
    rslt = configs['name'] + ' ' + configs['version']
    print(rslt)
    return ([rslt], pkgDir)

def _info(pkgDir):
    print(_getJSONData(os.path.join(pkgDir, 'package.json'))['description'])

def _grabDir(cwd):
    # this dir is listed as belonging to the package, so grab everything in it
    fileList = []
    for (subdir, dirs, files) in os.walk(cwd):
        for file_ in files:
            fileList.append(os.path.join(subdir,file_))

    return fileList
    
def _files(pkgDir):
    fileList = []
    for name in _getJSONData(os.path.join(pkgDir, 'package.json'))['files']:
        path = os.path.join(pkgDir,name)
        if (os.path.isdir(path)):
            fileList = fileList + _grabDir(path)
        else:
            fileList.append(path)

    print('\n'.join(fileList))
    return fileList
