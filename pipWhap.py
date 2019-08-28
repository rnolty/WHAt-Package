# adapted by nolty from github:nbeaver/pip_file_lookup, which has MIT license
# that code is Copyright (c) 2018 Nathaniel Morck Beaver

import os.path, subprocess
from functools import lru_cache

try:
    from pip.utils import get_installed_distributions
except ImportError:
    from pip._internal.utils.misc import get_installed_distributions

def executePlugin(args):
    # args was created by argparse, but more importantly it has boolean attributes 'info' and 'list'
    print("Trying pip:")
    packages = _find(args.file_full_path)
    [_info(package) for package in packages if args.info]
    [_files(package) for package in packages if args.list]

@lru_cache(maxsize=100)                     # remember output for each dist, in case we call again for -l files command
def _files_from_dist(dist):
    # dist should be a pip distribution class instance
    # RECORDs should be part of .dist-info metadatas
    if dist.has_metadata('RECORD'):
        lines = dist.get_metadata_lines('RECORD')
        paths = [l.split(',')[0] for l in lines]
        paths_absolute = [os.path.normpath(os.path.join(dist.location, p)) for p in paths]
    # Otherwise use pip's log for .egg-info's
    elif dist.has_metadata('installed-files.txt'):
        paths = dist.get_metadata_lines('installed-files.txt')
        paths_absolute = [os.path.normpath(os.path.join(dist.egg_info, p)) for p in paths]
    else:
        paths_absolute = []

    return paths_absolute

def _find(path):
    path = os.path.normpath(path)
    rslt = [dist for dist in get_installed_distributions() if path in _files_from_dist(dist)]
    [print(dist) for dist in rslt]
    return rslt


def _info(dist):
    # dist is probably "name-name version.version.version"
    dist_name = str(dist).split(' ')[0]
    [print(line) for line in subprocess.check_output(["pip", "show", dist_name], errors='ignore').split('\n')[:-1]]


def _files(dist):
    [print(file) for file in _files_from_dist(dist)]
