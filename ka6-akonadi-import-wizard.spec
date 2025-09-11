#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		akonadi-import-wizard
Summary:	Akonadi import wizard
Name:		ka6-%{kaname}
Version:	25.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c3373080125f7d4b5f6819381baf0ce8
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-kidentitymanagement-devel >= %{kdeappsver}
BuildRequires:	ka6-kmailtransport-devel >= %{kdeappsver}
BuildRequires:	ka6-libkdepim-devel >= %{kdeappsver}
BuildRequires:	ka6-mailcommon-devel >= %{kdeappsver}
BuildRequires:	ka6-mailimporter-devel >= %{kdeappsver}
BuildRequires:	ka6-messagelib-devel >= %{kdeappsver}
BuildRequires:	ka6-pimcommon-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kauth-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
ExcludeArch:	x32 i686
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Assistant to import PIM data from other applications into Akonadi for
use in KDE PIM applications.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6ImportWizard.so.*.*
%ghost %{_libdir}/libKPim6ImportWizard.so.6
%dir %{_libdir}/qt6/plugins/pim6/importwizard
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/balsaimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/clawsmailimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/evolutionv3importerplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/icedoveimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/seamonkeyimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/sylpheedimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/thunderbirdimporterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/importwizard/trojitaimporterplugin.so
%{_desktopdir}/org.kde.akonadiimportwizard.desktop
%{_iconsdir}/hicolor/128x128/apps/kontact-import-wizard.png
%{_iconsdir}/hicolor/256x256/apps/kontact-import-wizard.png
%{_iconsdir}/hicolor/64x64/apps/kontact-import-wizard.png
%{_datadir}/importwizard
%{_datadir}/qlogging-categories6/importwizard.categories
%{_datadir}/qlogging-categories6/importwizard.renamecategories

%files devel
%defattr(644,root,root,755)
%{_bindir}/akonadiimportwizard
%{_includedir}/KPim6/ImportWizard
%{_libdir}/cmake/KPim6ImportWizard
%{_libdir}/libKPim6ImportWizard.so
