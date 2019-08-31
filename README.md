# WHAt-Package
Search for the package that installed a file, across many package managers

```
$ whap.py /usr/bin/python
Trying RPM:
    python2-2.7.13-17.fc27.x86_64
Trying pip:
```

The --info command line switch:

```
$ whap.py -i /usr/bin/python 
Trying RPM:
    python2-2.7.13-17.fc27.x86_64

Name        : python2
Version     : 2.7.13
Release     : 17.fc27
Architecture: x86_64
...
Summary     : An interpreted, interactive, object-oriented programming language
Description :
Python 2 is an old version of the language that is incompatible with the 3.x
line of releases. The language is mostly the same, but many details, especially
how built-in objects like dictionaries and strings work, have changed
considerably, and a lot of deprecated features have finally been removed in the
3.x line.
...
This package provides the "python2" executable; most of the actual
implementation is within the "python2-libs" package.

Trying pip:
```

The --list command line switch (lists all files in the package)

```
$ whap.py -l /usr/bin/python 
Trying RPM:
    python2-2.7.13-17.fc27.x86_64

/usr/bin/pydoc
/usr/bin/pydoc2
/usr/bin/pydoc2.7
/usr/bin/python
/usr/bin/python2
/usr/bin/python2.7
/usr/lib/.build-id
/usr/lib/.build-id/21
/usr/lib/.build-id/21/5a79d63d8225814fbcc8985de34221a25ad86b
/usr/share/doc/python2
/usr/share/doc/python2/README
/usr/share/licenses/python2
/usr/share/licenses/python2/LICENSE
/usr/share/man/man1/python.1.gz
/usr/share/man/man1/python2.1.gz
/usr/share/man/man1/python2.7.1.gz

Trying pip:
```

To see available plugins, and choose which to use going forward, use the --config command line switch:

```
whap.py -c
Choose which package managers to search
rpm yN :y
pip yN :n
npm yN :y

Saving choices rpm,npm

```

```
whap.py /home/nolty/tmp.svg 
Trying RPM:
Trying npm:

```
