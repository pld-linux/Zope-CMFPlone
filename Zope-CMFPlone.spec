#
# Warning: This version (RC1) make errors on Zope (2.7b3) after AddPloneSite
# Recommended use stable version of Plone :)
#
%include	/usr/lib/rpm/macros.python
%define		zope_subname	CMFPlone
Summary:	Free and open source Content Management System based on Zope and CMF
Summary:	Darmowy i otwarty system zarz±dzania tre¶ci± oparty na Zope i CMF
Name:		Zope-%{zope_subname}
Version:	2.0
%define		sub_ver RC1 
Release:	5.%{sub_ver}.1
License:	Zope Public License (ZPL), GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/plone/%{zope_subname}%{version}-%{sub_ver}.tar.gz
# Source0-md5:	cd606b698247526073a6ad3a0ffa5579
Patch0:		%{name}-migration.patch
URL:		http://www.plone.org/
%pyrequires_eq	python-modules
Requires:	Zope-CMF >= 1.4
Requires:	Zope >= 2.6.2
Requires:	Zope-BTreeFolder2
Requires:	Zope-CMFQuickInstallerTool
Requires:	Zope-ExternalEditor
Requires:	Zope-Formulator
Requires:	Zope-GroupUserFolder >= 2.0
Requires(post,postun):	/usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	Plone
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
%setup -q -n %{zope_subname}-%{version}-%{sub_ver}
%patch0 -p1

%build
# remove dirs - additional packages!
rm -rf {BTreeFolder2,CMFQuickInstallerTool,ExternalEditor,GroupUserFolder,Formulator}

mkdir docs docs/CMFPlone docs/CMFFormController docs/i18n
rm -rf `find . type f -name .cvsignore`
mv -f CMFPlone/{CREDITS.txt,ChangeLog,HISTORY.txt,INSTALL.txt,README.txt} docs/CMFPlone
mv -f CMFPlone/docs/* docs/CMFPlone
mv -f CMFPlone/i18n/ChangeLog docs/i18n
rm -rf CMFPlone/i18n/{build.bat,msgfmt.exe}
mv -f CMFFormController/{AUTHORS,ChangeLog,README.txt} docs/CMFFormController
rm -rf CMFPlone/docs

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
for p in CMFPlone CMFActionIcons CMFFormController; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
	for p in CMFPlone CMFActionIcons CMFFormController; do
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
