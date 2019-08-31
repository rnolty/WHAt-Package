rpm:
	rpmbuild -bb --define "source_dir `pwd`" whap.spec
