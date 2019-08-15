# RPM plugin for whap (WHAt Package)

import subprocess

def Init():
    pass

def Find(fileFullPath):
    print("Trying RPM:")
    try:
        # passing a value for errors only to cause return value to be str, not bytes
        rslt = subprocess.check_output(['rpm','-qf',fileFullPath], errors='ignore')
    except subprocess.CalledProcessError:
        # probably it just didn't find anything, returned 1
        return []
    return str(rslt).split('\n')[:-1]        # kill the empty string due to trailing newline

def Info(package):
    try:
        return subprocess.check_output(['rpm','-qi',package], errors='ignore')
    except subprocess.CalledProcessError:
        return ''

def Files(package):
    try:
        return subprocess.check_output(['rpm','-ql',package], errors='ignore').split('\n')[:-1]
    except subprocess.CalledProcessError:
        return []


    
