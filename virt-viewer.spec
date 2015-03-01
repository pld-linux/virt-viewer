#
# Conditional build:
%bcond_with	gtk2	# use GTK+ 2.x instead of GTK+ 3.x
%bcond_without	spice	# SPICE support
%bcond_without	ovirt	# oVirt support
#
Summary:	Virtual Machine Viewer
Summary(pl.UTF-8):	Przeglądarka maszyny wirtualnej
Name:		virt-viewer
Version:	2.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	https://fedorahosted.org/released/virt-viewer/%{name}-%{version}.tar.gz
# Source0-md5:	4b1e9a2029e0dfff741e17bb915f75ec
URL:		http://virt-manager.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.14.1
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	intltool >= 0.35.0
%{?with_ovirt:BuildRequires:	libgovirt-devel >= 0.3.2}
BuildRequires:	libtool >= 2:2
BuildRequires:	libvirt-devel >= 0.10.0
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
BuildRequires:	spice-protocol >= 0.10.1
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	gtk-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk2-devel >= 0.22}
%else
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk3-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk-devel >= 0.22}
%endif
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires:	glib2 >= 1:2.22.0
Requires:	hicolor-icon-theme
Requires:	libvirt >= 0.10.0
Requires:	libxml2 >= 1:2.6.0
%if %{with gtk2}
Requires:	gtk+2 >= 2:2.18.0
Requires:	gtk-vnc >= 0.4.3
%{?with_spice:Requires: spice-gtk2 >= 0.22}
%else
Requires:	gtk+3 >= 3.0.0
Requires:	gtk3-vnc >= 0.4.3
%{?with_spice:Requires: spice-gtk >= 0.22}
%endif
%{?with_ovirt:Requires:	libgovirt >= 0.3.2}
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
	--disable-update-mimedb \
	%{__with_without spice spice-gtk} \
	--with-gtk=%{?with_gtk2:2.0}%{!?with_gtk2:3.0} \
	%{!?with_ovirt:--without-ovirt}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# empty version of ru,zh_CN,zh_TW
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ru_RU
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_CN.GB2312
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_TW.Big5

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_mime_database

%postun
%update_icon_cache hicolor
%update_mime_database

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
%{_iconsdir}/hicolor/24x24/devices/virt-viewer-usb.png
%{_iconsdir}/hicolor/24x24/devices/virt-viewer-usb.svg
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*
