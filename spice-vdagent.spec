# TODO:
# - package gdm files
#
# Conditional build:
%bcond_with	systemd	# use systemd instead of ConsoleKit for session tracking
#
Summary:	Linux guest agent for SPICE
Summary(pl.UTF-8):	Agent gościa linuksowego dla SPICE
Name:		spice-vdagent
Version:	0.21.0
Release:	0.1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	5e9862775240fc6f35b3109a21006fc6
Patch0:		%{name}-tmpfile.patch
URL:		https://www.spice-space.org/
BuildRequires:	alsa-lib-devel >= 1.0.22
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	glib2-devel >= 1:2.50
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libdrm-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	spice-protocol >= 0.14.3
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10
Requires:	alsa-lib >= 1.0.22
Requires:	glib2 >= 1:2.50
Requires:	gtk+3 >= 3.22
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libpciaccess >= 0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SPICE agent for Linux consists of 2 parts, a daemon spice-vdagentd
and a per X-session process spice-vdagent. The daemon gets
automatically started in Spice guests through a udev rule. The per
X-session gets automatically started in desktop environments which
honor /etc/xdg/autostart, and under gdm.

%description -l pl.UTF-8
Agent SPICE dla Linuksa składa się z 2 części: demona spice-vdagentd
oraz procesu dla sesji X spice-vdagent. Demon uruchamia się
automatycznie na gościach Spice poprzez regułę udeva. Proces dla sesji
X jest uruchamiany automatycznie w środowiskach graficznych
honorujących /etc/xdg/autostart oraz pod GDM-em.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-init-script=systemd+redhat \
	--with-session-info=%{?with_systemd:systemd}%{!?with_systemd:console-kit}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/spice-vdagent
%attr(755,root,root) %{_sbindir}/spice-vdagentd
# TODO: PLDify
%attr(754,root,root) /etc/rc.d/init.d/spice-vdagentd
/etc/xdg/autostart/spice-vdagent.desktop
%{systemdunitdir}/spice-vdagentd.service
%{systemdunitdir}/spice-vdagentd.socket
/lib/udev/rules.d/70-spice-vdagentd.rules
%{systemdtmpfilesdir}/spice-vdagentd.conf
%{_mandir}/man1/spice-vdagent.1*
%{_mandir}/man1/spice-vdagentd.1*
# TODO: gdm
#%{_datadir}/gdm/autostart/LoginWindow/spice-vdagent.desktop
#%{_datadir}/gdm/greeter/autostart/spice-vdagent.desktop
