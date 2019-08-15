#! /usr/bin/env python3

# adapted by nolty from github:nbeaver/pip_file_lookup, which has MIT license
# that code is Copyright (c) 2018 Nathaniel Morck Beaver

import os.path, subprocess

try:
    from pip.utils import get_installed_distributions
except ImportError:
    from pip._internal.utils.misc import get_installed_distributions

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

def Find(path):
    path = os.path.normpath(path)

    print("Trying pip:")
    dists = []
    for dist in get_installed_distributions():
        paths_absolute = _files_from_dist(dist)
        if (path in paths_absolute):
            dists.append(dist)

    return dists

def Info(dist):
    dist_name = dist.split(' ')[0]
    return subprocess.check_output(["pip", "show", dist_name])
