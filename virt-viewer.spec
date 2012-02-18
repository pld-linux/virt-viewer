#
# Conditional build:
%bcond_with	gtk2
%bcond_without	gtk3
%bcond_without	spice
%bcond_with	plugin
#
Summary:	Virtual Machine Viewer
Name:		virt-viewer
Version:	0.5.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://virt-manager.org/download/sources/virt-viewer/%{name}-%{version}.tar.gz
# Source0-md5:	69c82567df00afadfa2f79d3f1eb692d
URL:		http://virt-manager.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	glib2-devel
BuildRequires:	intltool >= 0.35.0
%if %{with gtk3}
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk3-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk-devel >= 0.9}
%endif
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2.12.0
BuildRequires:	gtk-vnc-devel >= 0.4.3
%{?with_spice:BuildRequires: spice-gtk2-devel >= 0.9}
%endif
BuildRequires:	libtool
BuildRequires:	libvirt-devel >= 0.6.0
BuildRequires:	libxml2-devel
BuildRequires:	perl-tools-pod
BuildRequires:	sed >= 4.0
%{?with_plugin:BuildRequires: xulrunner-devel}
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Suggests:	openssh-clients
Suggests:	gnome-keyring >= 0.4.9
ExclusiveArch:	%{ix86} x86_64 ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Machine Viewer provides a graphical console client for
connecting to virtual machines. It uses the GTK-VNC or SPICE-GTK
widgets to provide the display, and libvirt for looking up VNC/SPICE
server details.

Virtual Machine Viewer provides a graphical console client for
connecting to virtual machines. It uses the GTK-VNC or SPICE-GTK
widgets to provide the display, and libvirt for looking up VNC/SPICE
server details.

%package plugin
Summary:	Mozilla plugin for the gtk-vnc library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin
Virtual Machine Viewer provides a graphical
console client for connecting to virtual machines. It uses the GTK-VNC
or SPICE-GTK widgets to provide the display, and libvirt for looking
up VNC/SPICE server details.

This package provides a web browser plugin for Mozilla compatible
browsers.

%prep
%setup -q

%{__sed} -i -e 's|PWD|shell pwd|g' icons/*/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{__enable_disable plugin} \
	%{__with_without spice spice-gtk} \
	%{__with_without gtk2 gtk 2.0} \
	%{__with_without gtk3 gtk 3.0}

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
%{_iconsdir}/hicolor/*/apps/virt-viewer.png
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*

%if %{with plugin}
%files plugin
%defattr(644,root,root,755)
%endif
