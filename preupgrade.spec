%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Summary: Preresolves dependencies and prepares a system for an upgrade
Name: preupgrade
Version: 0.9.8
Release: 2%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: https://fedorahosted.org/releases/p/r/preupgrade/%{name}-%{version}.tar.gz
Patch1: preupgrade-0.9.8-fix-resume.patch
Patch2: preupgrade-0.9.8-f10beta.patch
URL: https://fedorahosted.org/preupgrade/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python >= 2.1, rpm-python, rpm >= 0:4.1.1
Requires: pyxf86config
# preupgrade-gui requires pygtk2 and libglade
# FIXME: split out preupgrade-gtk subpackage that requires this
Requires: pygtk2-libglade
# F10 anaconda provides its special depsolving magic as yum plugins
Requires: anaconda-yum-plugins
# F10 anaconda expects to be handed a valid yum repo
Requires: createrepo
# yum 3.2.18 is needed to enable the above plugins at runtime
Requires: yum-metadata-parser, yum >= 3.2.18
Requires: usermode
Requires: e2fsprogs
Requires(post): mkinitrd
BuildRequires: desktop-file-utils, python

%description
Preresolves all dependencies, downloads the packages and makes your system 
ready for an upgrade via anaconda.

%prep
%setup -q
%patch1 -p1 -b .fix-resume
%patch2 -p1 -b .f10beta

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
* Thu Oct  2 2008 Will Woods <wwoods@redhat.com> - 0.9.8-2
- Clear cache after user decides not to resume an old run
- Add Fedora 10 Beta to releases.list

* Thu Sep 18 2008 Will Woods <wwoods@redhat.com> - 0.9.8-1
- GUI version prompts to resume interrupted runs
- Checks for available disk space before downloading / rebooting
- Does not change boot target until you hit the Reboot button
- Handle invalid treeinfo gracefully (bug #459935)
- Use UUID=xxx for devices - makes finding devices much more robust
- No more network dialog for missing packages
- Use anaconda's own depsolving tweaks (whiteout/blacklist)
- Use kickstart to automate installs

* Tue May  6 2008 Will Woods <wwoods@redhat.com> - 0.9.3-2
- Add missing Requires on pyxf86config

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
