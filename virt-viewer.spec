#
# Conditional build:
%bcond_with	gtk2	# use GTK+ 2.x instead of GTK+ 3.x
%bcond_without	spice	# SPICE support
%bcond_with	ovirt	# oVirt support [requiring libgovirt, depending on rest >= 1.7.13]
#
Summary:	Virtual Machine Viewer
Summary(pl.UTF-8):	Przeglądarka maszyny wirtualnej
Name:		virt-viewer
Version:	0.5.7
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://virt-manager.org/download/sources/virt-viewer/%{name}-%{version}.tar.gz
# Source0-md5:	c0d6d2de66e61df6c2ad339625c58a2a
URL:		http://virt-manager.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	intltool >= 0.35.0
%{?with_ovirt:BuildRequires:	libgovirt-devel >= 0.1.0}
BuildRequires:	libtool >= 2:2
BuildRequires:	libvirt-devel >= 0.10.0
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	perl-tools-pod
BuildRequires:	sed >= 4.0
BuildRequires:	spice-protocol >= 0.10.1
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	gtk-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk2-devel >= 0.20}
%else
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk3-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk-devel >= 0.20}
%endif
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.22.0
Requires:	hicolor-icon-theme
Requires:	libvirt >= 0.10.0
Requires:	libxml2 >= 1:2.6.0
%if %{with gtk2}
Requires:	gtk+2 >= 2:2.18.0
Requires:	gtk-vnc >= 0.4.3
%{?with_spice:Requires: spice-gtk2 >= 0.20}
%else
BuildRequires:	gtk+3 >= 3.0.0
BuildRequires:	gtk3-vnc >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk >= 0.20}
%endif
%{?with_ovirt:Requires:	libgovirt >= 0.1.0}
Suggests:	openssh-clients
Suggests:	gnome-keyring >= 0.4.9
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
	%{__with_without spice spice-gtk} \
	--with-gtk=%{?with_gtk2:2.0}%{!?with_gtk2:3.0} \
	%{!?with_ovirt:--without-ovirt}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/virt-viewer
%attr(755,root,root) %{_bindir}/remote-viewer
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*.xml
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_desktopdir}/remote-viewer.desktop
%{_iconsdir}/hicolor/*/apps/virt-viewer.png
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*
