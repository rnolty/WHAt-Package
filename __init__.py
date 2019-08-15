# WHAt Package?
#
# v0.0.1
#
# whap is used to find out which, if any, of several package managers
#    has installed a file on your computer

plugins = {'rpm': 'rpmWhap', 'pip': 'pipWhap'}

# todo: add more plugins: dpkg, cpan, pear, docker, flatpak, apm (atom editor)
#       my python2.7 version of subprocess doesn't support errors argument; not
#          sure what I have to do to get byte string returned by check_output
#          into a str.  Short of that I think runs equally well under python2
#          or python3; difference is that pip database applies only to the
#          version of python running
#       Figure out how to check both pip2 and pip3
