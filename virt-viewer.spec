#
# Conditional build:
%bcond_without	spice	# SPICE support
%bcond_without	ovirt	# oVirt support
#
Summary:	Virtual Machine Viewer
Summary(pl.UTF-8):	Przeglądarka maszyny wirtualnej
Name:		virt-viewer
Version:	9.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	https://virt-manager.org/download/sources/virt-viewer/%{name}-%{version}.tar.gz
# Source0-md5:	f90413f321b697405369c6f963ea7a5e
URL:		http://virt-manager.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.14.1
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gtk+3-devel >= 3.12
BuildRequires:	gtk3-vnc-devel >= 0.4.3
BuildRequires:	icoutils
BuildRequires:	intltool >= 0.35.0
%{?with_ovirt:BuildRequires:	libgovirt-devel >= 0.3.3}
BuildRequires:	libtool >= 2:2
BuildRequires:	libvirt-devel >= 1.2.8
BuildRequires:	libvirt-glib-devel >= 0.1.8
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_ovirt:BuildRequires:	rest-devel >= 0.8}
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
%{?with_spice:BuildRequires:	spice-gtk-devel >= 0.35}
BuildRequires:	spice-protocol >= 0.12.7
BuildRequires:	vte-devel
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires:	glib2 >= 1:2.40.0
Requires:	gtk+3 >= 3.12
Requires:	gtk3-vnc >= 0.4.3
Requires:	hicolor-icon-theme
%{?with_ovirt:Requires:	libgovirt >= 0.3.3}
Requires:	libvirt >= 1.2.8
Requires:	libvirt-glib >= 0.1.8
Requires:	libxml2 >= 1:2.6.0
%{?with_ovirt:Requires:	rest >= 0.8}
%{?with_spice:Requires:	spice-gtk >= 0.35}
Suggests:	gnome-keyring >= 0.4.9
Suggests:	openssh-clients
# let it obsolete withdrawn spice client from spice-space package
%{?with_spice:Obsoletes:	spice-client}
Obsoletes:	virt-viewer-plugin
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Machine Viewer provides a graphical console client for
connecting to virtual machines. It uses the GTK-VNC or SPICE-GTK
widgets to provide the display, and libvirt for looking up VNC/SPICE
server details.

%description -l pl.UTF-8
Virtual Machine Viewer udostępnia klienta graficznej konsoli do
łączenia z maszynami wirtualnymi. Wykorzystuje widgety GTK-VNC lub
SPICE-GTK do zapewnienia obrazu oraz libvirt do odczytu szczegółów
serwera VNC/SPICE.

%package -n bash-completion-virt-viewer
Summary:	bash-completion for virt-viewer command
Summary(pl.UTF-8):	bashowe uzupełnianie parametrów polecenia virt-viewer
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-virt-viewer
Bash-completion for virt-viewer command.

%description -n bash-completion-virt-viewer -l pl.UTF-8
Bashowe uzupełnianie parametrów polecenia virt-viewer.

%prep
%setup -q

%{__sed} -i -e 's|PWD|shell pwd|g' icons/*/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-update-mimedb \
	%{__with_without spice spice-gtk} \
	%{!?with_ovirt:--without-ovirt}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

#%clean
#rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_mime_database

%postun
%update_icon_cache hicolor
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_bindir}/virt-viewer
%attr(755,root,root) %{_bindir}/remote-viewer
%{_datadir}/appdata/remote-viewer.appdata.xml
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_desktopdir}/remote-viewer.desktop
%{_iconsdir}/hicolor/*/apps/virt-viewer.png
%{_iconsdir}/hicolor/24x24/devices/virt-viewer-usb.png
%{_iconsdir}/hicolor/24x24/devices/virt-viewer-usb.svg
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*

%files -n bash-completion-virt-viewer
%defattr(644,root,root,755)
%{bash_compdir}/virt-viewer
