Name:           whap
Version:        0.1
Release:        4%{?dist}
Summary:        Queries several package managers to learn which, if any, installed a given file

License:        GPLv3+
URL:            https://github.com/rnolty/WHAt-Package

BuildRequires:  python3
Requires:       python3
Requires:       bash
BuildArch:      noarch


%define __python /usr/bin/python3    # so automatic byte compile won't use python2

%description

   whap stands for WHAt Package, and helps determine if a file in the
   filesystem was installed by a package manager (such as RPM, npm, pip,
   etc.); additionally, whap can print the description of the package (if
   provided by the package manager) and list other files from the same
   package.

   Usage:
   whap [--info|-i] [--list|-l] <file path>
   what [--config|-c]






%install
   # source_dir must be passed on command line, as in
   # rpmbuild -bb --define "source_dir `pwd`" whap.spec
   cd %{source_dir}
   #python3 -m compileall *.py       # RPM does this automatically

   mkdir -p %{buildroot}/%{_bindir}
   mkdir -p %{buildroot}/usr/lib/%{name}
   cat > %{buildroot}/%{_bindir}/%{name} <<-EOF
#!/bin/bash
python3 /usr/lib/%{name}/%{name}.py \$*
EOF
   chmod 0755 %{buildroot}/%{_bindir}/%{name}
   install -m 0644 *.py* %{buildroot}/usr/lib/%{name}/
   mkdir -- %{buildroot}/usr/lib/%{name}/__pycache__
   install -m 0644 __pycache__/* %{buildroot}/usr/lib/%{name}/__pycache__
   mkdir -p %{buildroot}/usr/share/doc/whap
   install -m 0644 README.md  %{buildroot}/usr/share/doc/whap/
   mkdir -p %{buildroot}/usr/share/licenses/whap
   install -m 0644 LICENSE  %{buildroot}/usr/share/licenses/whap/


%files
   %license LICENSE
   %doc README.md

   %dir /usr/lib/%{name}/
   %{_bindir}/%{name}
   /usr/lib/%{name}/*.py*
   /usr/lib/%{name}/__pycache__/*.pyc



%changelog
* Wed Aug 28 2019 Bob Nolty <nolty@BobDelF27> 0.1-1
- 1st package of still-in-progress software
