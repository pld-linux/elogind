Summary:	Elogind User, Seat and Session Manager
Summary(pl.UTF-8):	Elogind - zarządca użytkowników, stanowisk i sesji
Name:		elogind
Version:	252.9
Release:	2
License:	LGPL v2.1+
Group:		Daemons
# Source0Download: https://github.com/elogind/elogind/releases
Source0:	https://github.com/elogind/elogind/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2be2c43298e2fc41c5bee33dde605f01
URL:		https://github.com/elogind/elogind
BuildRequires:	acl-devel
BuildRequires:	audit-libs-devel
BuildRequires:	dbus-devel >= 1.4.0
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-tools
# checked, but finally not used
#BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gperf
BuildRequires:	libcap-devel
BuildRequires:	libmount-devel >= 2.30
BuildRequires:	libselinux-devel >= 2.1.9
BuildRequires:	m4
BuildRequires:	meson >= 0.53.2
BuildRequires:	ninja
BuildRequires:	pam-devel >= 1:1.1.2
BuildRequires:	pcre2-8-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.727
BuildRequires:	udev-devel >= 1:185
BuildConflicts:	polkit-devel < 0.106
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.4.0
Requires:	glib2 >= 1:2.22.0
Requires:	libmount >= 2.30
Requires:	pam >= 1:1.3.0-3
Requires:	udev-core >= 1:185
Conflicts:	systemd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_rootbindir	/bin

%description
Elogind is the systemd project's "logind", extracted out to be a
standalone daemon. It integrates with PAM to know the set of users
that are logged in to a system and whether they are logged in
graphically, on the console, or remotely. Elogind exposes this
information via the standard org.freedesktop.login1 D-Bus interface,
as well as through the file system using systemd's standard
/run/systemd layout. Elogind also provides "libelogind", which is a
subset of the facilities offered by "libsystemd".

%description -l pl.UTF-8
Elogind to część "logind" z projektu systemd wydzielona jako
samodzielny demon. Integruje się z PAM, aby znać listę użytkowników
zalogowanych do systemu oraz wiedzieć, czy są zalogowani graficznie,
na konsoli, czy zdalnie. Elogind udostępnia te informacje poprzez
standardowy interfejs D-Bus org.freedesktop.login1, a także poprzez
system plików, wykorzystując układ /run/systemd zgodny z systemd.
Elogind dostarcza także bibliotekę libelogind, będącą podzbiorem
funkcjonalności oferowanej przeez libsystemd.

%package -n bash-completion-elogind
Summary:	Bash completion for loginctl command
Summary(pl.UTF-8):	Bashowe dopełnianie składni polecenia loginctl
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
Conflicts:	bash-completion-systemd
BuildArch:	noarch

%description -n bash-completion-elogind
Bash completion for loginctl command.

%description -n bash-completion-elogind -l pl.UTF-8
Bashowe dopełnianie składni polecenia loginctl.

%package -n zsh-completion-elogind
Summary:	zsh completion for loginctl command
Summary(pl.UTF-8):	Uzupełnianie parametrów w zsh dla polecenia loginctl
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
Conflicts:	zsh-completion-systemd
BuildArch:	noarch

%description -n zsh-completion-elogind
zsh completion for loginctl command.

%description -n zsh-completion-elogind -l pl.UTF-8
Uzupełnianie parametrów w zsh dla polecenia loginctl.

%package libs
Summary:	Shared elogind library
Summary(pl.UTF-8):	Biblioteka współdzielona elogind
Group:		Libraries

%description libs
Shared elogind library.

%description libs -l pl.UTF-8
Biblioteka współdzielona elogind.

%package devel
Summary:	Header files for elogind library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki elogind
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for elogind library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki elogind.

%prep
%setup -q

%build
%meson build \
	-Dhalt-path=/sbin/halt \
	-Dkexec-path=/sbin/kexec \
	-Dnologin-path=/sbin/nologin \
	-Dpoweroff-path=/sbin/poweroff \
	-Dreboot-path=/sbin/reboot \
	-Dpamconfdir=/%{_sysconfdir}/pam.d \
	-Dpamlibdir=/%{_lib}/security \
	-Drootlibdir=%{_libdir} \
	-Drootlibexecdir=%{_libexecdir}/%{name} \
	-Dsplit-bin=true \
	-Dsplit-usr=true \
	-Dman=true

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/elogind/system-{shutdown,sleep}/.keep_dir

# provided by systemd-devel
%{__rm} \
	$RPM_BUILD_ROOT%{_mandir}/man3/SD_*.3 \
	$RPM_BUILD_ROOT%{_mandir}/man3/sd_*.3 \
	$RPM_BUILD_ROOT%{_mandir}/man3/sd-*.3

# provided by udev-core
%{__rm} $RPM_BUILD_ROOT/lib/udev/rules.d/70-power-switch.rules

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md TODO
%dir %{_sysconfdir}/elogind
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/elogind/logind.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/elogind/sleep.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/elogind-user
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
%attr(755,root,root) /%{_lib}/security/pam_elogind.so
%attr(755,root,root) %{_bindir}/busctl
%attr(755,root,root) %{_rootbindir}/loginctl
%attr(755,root,root) %{_rootbindir}/elogind-inhibit
%dir %{_libexecdir}/elogind
%attr(755,root,root) %{_libexecdir}/elogind/elogind
%attr(755,root,root) %{_libexecdir}/elogind/elogind-cgroups-agent
%attr(755,root,root) %{_libexecdir}/elogind/elogind-uaccess-command
%dir %{_libdir}/elogind
%attr(755,root,root) %{_libdir}/elogind/libelogind-shared-%{version}.so
%dir %{_libexecdir}/elogind/system-shutdown
%dir %{_libexecdir}/elogind/system-sleep
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_mandir}/man1/busctl.1*
%{_mandir}/man1/elogind-inhibit.1*
%{_mandir}/man1/loginctl.1*
%{_mandir}/man5/logind.conf.5*
%{_mandir}/man5/logind.conf.d.5*
%{_mandir}/man5/org.freedesktop.login1.5*
%{_mandir}/man5/sleep.conf.5*
%{_mandir}/man5/sleep.conf.d.5*
%{_mandir}/man7/elogind.directives.7*
%{_mandir}/man7/elogind.index.7*
%{_mandir}/man7/elogind.journal-fields.7*
%{_mandir}/man7/elogind.syntax.7*
%{_mandir}/man7/elogind.time.7*
%{_mandir}/man8/elogind.8*
%{_mandir}/man8/pam_elogind.8*

%files -n bash-completion-elogind
%defattr(644,root,root,755)
%{bash_compdir}/busctl
%{bash_compdir}/loginctl

%files -n zsh-completion-elogind
%defattr(644,root,root,755)
%{zsh_compdir}/_busctl
%{zsh_compdir}/_loginctl

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelogind.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelogind.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelogind.so
%{_includedir}/elogind
%{_pkgconfigdir}/libelogind.pc
