# RPM plugin for whap (WHAt Package)
# We just run the rpm executable in a subprocess

import subprocess

def executePlugin(args):
    # args was created by argparse, but more importantly it has boolean attributes 'info' and 'list'
    print("Trying RPM:")
    packages = _find(args.file_full_path)
    [_info(package) for package in packages if args.info]
    [_files(package) for package in packages if args.list]

def _find(fileFullPath):
    try:
        # passing a value for errors only to cause return value to be str, not bytes
        rslt = subprocess.check_output(['rpm','-qf',fileFullPath], errors='ignore')
    except subprocess.CalledProcessError:
        # probably it just didn't find anything, returned 1
        return []
    print(rslt)
    return rslt.split('\n')[:-1]         # kill the empty string due to trailing newline

def _info(package):
    try:
        print(subprocess.check_output(['rpm','-qi',package], errors='ignore'))
    except subprocess.CalledProcessError:
        return ''

def _files(package):
    try:
        print(subprocess.check_output(['rpm','-ql',package], errors='ignore'))
    except subprocess.CalledProcessError:
        pass
