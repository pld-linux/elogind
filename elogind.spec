Summary:	Elogind User, Seat and Session Manager
Summary(pl.UTF-8):	Elogind - zarządca użytkowników, stanowisk i sesji
Name:		elogind
Version:	231.3
Release:	0.2
License:	LGPL v2.1+
Group:		Daemons
# Source0Download: https://github.com/elogind/elogind/releases
Source0:	https://github.com/elogind/elogind/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ffc16ab3ae77254cc3d02af37ea463bb
URL:		https://github.com/elogind/elogind
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.4.0
BuildRequires:	gcc >= 5:3.2
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gperf
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libapparmor-devel
BuildRequires:	libblkid-devel >= 2.24
BuildRequires:	libcap-devel
BuildRequires:	libmount-devel >= 2.20
BuildRequires:	libseccomp-devel >= 1.0.0
BuildRequires:	libselinux-devel >= 2.1.9
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxslt-progs
BuildRequires:	pam-devel >= 1:1.1.2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.719
BuildRequires:	udev-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.4.0
Requires:	udev-core >= 1:185
Conflicts:	systemd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
#install -d docs
#%{__gtkdocize} --docdir docs --flavour no-tmpl
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	HALT=/sbin/halt \
	KEXEC=/sbin/kexec \
	REBOOT=/sbin/reboot \
	--disable-silent-rules \
	--enable-split-usr \
	--with-pamlibdir=/%{_lib}/security

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libelogind.la \
	$RPM_BUILD_ROOT/%{_lib}/security/*.la

# provided by systemd-devel
%{__rm} \
	$RPM_BUILD_ROOT%{_mandir}/man3/SD_*.3 \
	$RPM_BUILD_ROOT%{_mandir}/man3/sd_*.3 \
	$RPM_BUILD_ROOT%{_mandir}/man3/sd-*.3

# provided by udev-core
%{__rm} $RPM_BUILD_ROOT/lib/udev/rules.d/70-power-switch.rules

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENSE.MIT NEWS README TODO src/libelogind/sd-bus/{DIFFERENCES,GVARIANT-SERIALIZATION,PORTING-DBUS1}
%dir %{_sysconfdir}/elogind
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/elogind/logind.conf
/etc/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/elogind-user
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
%attr(755,root,root) /%{_lib}/security/pam_elogind.so
%attr(755,root,root) %{_bindir}/loginctl
%attr(755,root,root) %{_bindir}/elogind-inhibit
%dir %{_libexecdir}/elogind
%attr(755,root,root) %{_libexecdir}/elogind/elogind
%attr(755,root,root) %{_libexecdir}/elogind/elogind-cgroups-agent
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_mandir}/man1/loginctl.1*
%{_mandir}/man5/logind.conf.5*
%{_mandir}/man7/elogind.directives.7*
%{_mandir}/man7/elogind.index.7*
%{_mandir}/man8/elogind.8*
%{_mandir}/man8/pam_elogind.8*

%files -n bash-completion-elogind
%defattr(644,root,root,755)
%{bash_compdir}/loginctl

%files -n zsh-completion-elogind
%defattr(644,root,root,755)
%{zsh_compdir}/_elogind-inhibit
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
