%include	/usr/lib/rpm/macros.python
%define		zope_subname Plone
Summary:	A free, open source Content Management System based on Zope and CMF
Summary:	Darmowy, otwarty system zarz±dzania tre¶ci± oparty na Zope i CMF
Name:		Zope-CMF%{zope_subname}
Version:	1.0.5
Release:	7
License:	Zope Public License (ZPL), GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/plone/CMF%{zope_subname}%{version}.tar.gz
# Source0-md5:	942dbc488e6fb15c356e010076857999
URL:		http://www.plone.org/
%pyrequires_eq	python-modules
Requires:	Zope-CMF <= 1.4
Requires:	Zope
Requires:	Zope-Formulator
Requires(post,postun):  /usr/sbin/installzopeproduct
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
%setup -q -n CMF%{zope_subname}-%{version}

%build
# remove dir - additional packages!
rm -rf Formulator

rm -rf `find . -type f -name .cvsignore`
mkdir docs docs/DCWorkflow docs/i18n
mv -f CMFPlone/*.txt docs/
mv -f CMFPlone/docs/*.txt docs/
rm -rf CMFPlone/docs
mv -f CMFPlone/ChangeLog docs/
mv -f DCWorkflow/*.txt docs/DCWorkflow
mv -f i18n/ChangeLog docs/i18n
rm -rf i18n/{build.bat,msgfmt.exe}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFPlone DCWorkflow i18n ; do
        /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
    /etc/rc.d/init.d/zope restart >&2
fi

echo "From /manage interface there should be a 'Select Type to Add' and says Plone Site"
echo "The default Plone administrator userid is 'admin' with password 'plone'." >&2

%postun
for p in CMFPlone DCWorkflow i18n ; do
      /usr/sbin/installzopeproduct -d $p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
