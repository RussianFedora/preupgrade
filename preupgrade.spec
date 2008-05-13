%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Summary: Preresolves dependencies and prepares a system for an upgrade
Name: preupgrade
Version: 0.9.3
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: https://fedorahosted.org/releases/p/r/preupgrade/%{name}-%{version}.tar.gz
Patch0: enable-f9.patch
Patch1: retrieve-treeinfo-from-instrepo.patch
URL: https://fedorahosted.org/preupgrade/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python >= 2.1, rpm-python, rpm >= 0:4.1.1
Requires: yum-metadata-parser, yum >= 3.2.8
Requires: usermode
Requires(post): mkinitrd
BuildRequires: desktop-file-utils, python

%description
Preresolves all dependencies, downloads the packages and makes your system 
ready for an upgrade via anaconda.

%prep
%setup -q
%patch0 -p0
%patch1 -p0 

%build
# no op

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
ln -s consolehelper $RPM_BUILD_ROOT/%{_bindir}/%{name}
ln -s consolehelper $RPM_BUILD_ROOT/%{_bindir}/%{name}-cli

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/grubby --remove-kernel=/boot/upgrade/vmlinuz
%{__rm} -rf /boot/upgrade

%files
%defattr(-, root, root)
%dir %{_datadir}/%{name}
%doc ChangeLog README COPYING
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%{_datadir}/%{name}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}-cli
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{python_sitelib}/%{name}

%changelog
* Tue May 13 2008 Will Woods <wwoods@redhat.com> - 0.9.3-3
- Fix hang on "Downloading installer metadata" (bug #446244)

* Tue May 13 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.3-2
- enable F9 in releases.list

* Fri May  2 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.3-1
- 0.9.3


* Thu May  1 2008 Seth Vidal <skvidal at fedoraproject.org> 
- make preupgrade clean up its messes in %post so it doesn't leave
  cruft on the fs after an upgrade.

* Thu Apr 24 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.2-1
- 0.9.2 
- put cli tool back in 

* Mon Apr 21 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.1-1
- 0.9.1

* Mon Apr  7 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9-2
- add dist tag
- fix buildroot
- fix buildarchitectures to buildarch


* Thu Apr  3 2008 Will Woods <wwoods@redhat.com> - 0.9-1
- Remove .desktop file; we'll run from a puplet notification (or by hand)
- Check file size on downloaded boot images to make sure they're the right ones
- More descriptive title for boot item
- Update releases.list - add Fedora 9 Beta
- Add python as a buildreq 

* Wed Mar 26 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.8-1
- remove the cli for now b/c it is broken!

* Mon Mar 24 2008 Will Woods <wwoods@redhat.com> - 0.8-1
- Functionally nearly complete
- Add .desktop file for GUI

* Thu Feb  7 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.1-1
- first pkging attempt
