%include	/usr/lib/rpm/macros.python
%define		zope_subname	CMFPlone
Summary:	Free and open source Content Management System based on Zope and CMF
Summary:	Darmowy i otwarty system zarz�dzania tre�ci� oparty na Zope i CMF
Name:		Zope-%{zope_subname}
Version:	1.0.5
Release:	1
License:	Zope Public License (ZPL), GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/plone/%{zope_subname}%{version}.tar.gz
URL:		http://www.plone.org/
%pyrequires_eq	python-modules
Requires:	Zope-CMF >= 1.3.3
Requires:	Zope-CMF < 1.4
Requires:	Zope >= 2.6.2
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
Plone jest darmowym systemem zarz�dzania informacj� z otwartym kodem
�r�d�owym. G��wnym celem Plone jest mo�liwo�� dzielenia si� informacj�
na ka�dym poziomie dost�pu. Jest to "silnik" serwisu umo�liwiaj�cy
prac� z wieloma j�zykami, z wst�pn� konfiguracj� uwzgl�dniaj�c�
zabezpieczenia serwisu. Plone dzia�a w zestawie z CMF, Zope i
Pythonem.

%prep
%setup -q -n %{zope_subname}-%{version}

%build
# remove dirs - additional packages!
rm -rf {BTreeFolder2,CMFQuickInstallerTool,ExternalEditor,GroupUserFolder,Formulator}

mkdir docs docs/CMFPlone docs/CMFFormController docs/i18n
mv -f CMFPlone/{CREDITS.txt,ChangeLog,HISTORY.txt,INSTALL.txt,README.txt} docs/CMFPlone
mv -f CMFPlone/docs/* docs/CMFPlone
mv -f i18n/ChangeLog docs/i18n
rm -rf i18n/{build.bat,msgfmt.exe}
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
for p in CMFPlone DCWorkflow; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi
echo "From /manage interface there should be a 'Select Type to Add' and says Plone Site" >&2

%postun
if [ "$1" = "0" ]; then
	for p in CMFPlone DCWorkflow; do
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
