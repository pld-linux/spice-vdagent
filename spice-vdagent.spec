#
# Conditional build:
%bcond_with	systemd	# use systemd instead of ConsoleKit for session tracking
#
Summary:	Linux guest agent for SPICE
Summary(pl.UTF-8):	Agent gościa linuksowego dla SPICE
Name:		spice-vdagent
Version:	0.10.1
Release:	0.1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	0e69a13e4df37eefb52b1df795b22755
URL:		http://spice-space.org/
%{!?with_systemd:BuildRequires:	ConsoleKit-devel}
BuildRequires:	dbus-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	spice-protocol >= 0.8.0
%{?with_systemd:BuildRequires:	systemd-devel >= 42}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10
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

%build
%configure \
	--disable-silent-rules \
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
%doc ChangeLog README TODO
%attr(755,root,root) %{_bindir}/spice-vdagent
%attr(755,root,root) %{_sbindir}/spice-vdagentd
# TODO: PLDify
%attr(754,root,root) /etc/rc.d/init.d/spice-vdagentd
# XXX: should be /usr/lib/tmpfiles.d?
/etc/tmpfiles.d/spice-vdagentd.conf
/etc/xdg/autostart/spice-vdagent.desktop
#%{_datadir}/gdm/autostart/LoginWindow/spice-vdagent.desktop
