
%define		zope_subname	CMFPlone
Summary:	Free and open source Content Management System based on Zope and CMF
Summary(pl):	Darmowy i otwarty system zarz±dzania tre¶ci± oparty na Zope i CMF
Name:		Zope-%{zope_subname}
Version:	2.1.1
Release:	1
License:	Zope Public License (ZPL), GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/plone/Plone-%{version}.tar.gz
# Source0-md5:	c6f013fbb8822d13ca958e68346ad22d
URL:		http://www.plone.org/
BuildRequires:	python
%pyrequires_eq	python-modules
Requires:	i18ndude
Requires:	python-Imaging
Requires:	Zope-archetypes >= 1.3.4
Requires:	Zope-kupu >= 1.3
Requires:	Zope-CMF = 1:1.5.4
Requires:	Zope >= 2.7.7
Requires:	Zope-BTreeFolder2 >= 1.0.2
Requires:	Zope-CMFQuickInstallerTool >= 1.5.5
Requires:	Zope-Epoz >= 0.8.2
Requires:	Zope-ExternalEditor >= 0.9.1
Requires:	Zope-Formulator >= 1.6.2
Requires:	Zope-GroupUserFolder >= 1:3.4
Requires:	Zope-PlacelessTranslationService >= 1.2.1
Requires:	Zope-PloneLanguageTool >= 0.7
Requires(post,postun):	/usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	Plone
Obsoletes:	Zope-PortalTransforms
Conflicts:	CMF

%description
Plone is a free, open source Content Management System. The focus of
Plone is to provide value at every level of an organization. It comes
with a workflow engine, pre-configured security and roles, a set of
content types and multi-lingual support. There are many developers,
writers and testers from all over the world, contributing to Plone
everyday. Plone is based on the Content Management Framework.

%description -l pl
Plone jest darmowym systemem zarz±dzania informacj± z otwartym kodem
¼ród³owym. G³ównym celem Plone jest mo¿liwo¶æ dzielenia siê informacj±
na ka¿dym poziomie dostêpu. Jest to "silnik" serwisu umo¿liwiaj±cy
pracê z wieloma jêzykami, z wstêpn± konfiguracj± uwzglêdniaj±c±
zabezpieczenia serwisu. Plone dzia³a w zestawie z CMF, Zope i
Pythonem.

%prep
%setup -q -n Plone-%{version}
# remove dirs - additional packages!
# ExternalEditor
rm -rf {BTreeFolder2,CMFQuickInstallerTool,Formulator,GroupUserFolder,Archetypes,generator,validation}
rm -rf {PloneLanguageTool,kupu,MimetypesRegistry}
rm -rf {CMFActionIcons,CMFSetup,CMFUid}
rm -rf {CMFCalendar,CMFCore,CMFDefault,CMFTopic,DCWorkflow,PortalTransforms,Epoz}
rm -rf {ExternalEditor,PlacelessTranslationService}
find . -type d -name debian | xargs rm -rf

%build
mkdir docs docs/CMFPlone docs/CMFFormController docs/PloneErrorReporting
mv -f CMFPlone/{CREDITS.txt,HISTORY.txt,INSTALL.txt,README.txt,UPGRADE.txt,LICENSE.txt} docs/CMFPlone
rm -rf CMFPlone/LICENSE.GPL
mv -f CMFFormController/{AUTHORS,ChangeLog,README.txt} docs/CMFFormController
rm -rf CMFPlone/docs
mv -f PloneErrorReporting/{ChangeLog,README.txt} docs/PloneErrorReporting
rm -rf PloneErrorReporting/LICENSE.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in ATContentTypes ATReferenceBrowserWidget CMFDynamicViewFTI CMFFormController CMFPlone ExtendedPathIndex; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
for p in PloneErrorReporting PloneTranslations ResourceRegistries SecureMailHost; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done  

if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
	for p in ATContentTypes ATReferenceBrowserWidget CMFDynamicViewFTI CMFFormController CMFPlone ExtendedPathIndex; do
		/usr/sbin/installzopeproduct -d $p
	done
	for p in PloneErrorReporting PloneTranslations ResourceRegistries SecureMailHost; do
		/usr/sbin/installzopeproduct -d $p
	done
	if [ -f /var/lock/subsys/zope ]; then
		/etc/rc.d/init.d/zope restart >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
