%include	/usr/lib/rpm/macros.python
%define		zope_subname Plone
Summary:	A free, open source Content Management System based on Zope and CMF
Summary:	Darmowy, otwarty system zarz±dzania tre¶ci± oparty na Zope i CMF
Name:		Zope-CMF%{zope_subname}
Version:	1.0.5
Release:	5
License:	Zope Public License (ZPL), GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/plone/CMF%{zope_subname}%{version}.tar.gz
# Source0-md5:	942dbc488e6fb15c356e010076857999
URL:		http://www.plone.org/
%pyrequires_eq	python-modules
Requires:	CMF <= 1.4
Requires:	Zope
Requires:	Zope-Formulator
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{zope_subname}-%{version}-root-%(id -u -n)

%define		product_dir	/usr/lib/zope/Products

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
# remove dir - additional spec!
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
install -d $RPM_BUILD_ROOT%{product_dir}
cp -af * $RPM_BUILD_ROOT%{product_dir}

%py_comp $RPM_BUILD_ROOT%{product_dir}
%py_ocomp $RPM_BUILD_ROOT%{product_dir}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{product_dir}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/zope ]; then
    /etc/rc.d/init.d/zope restart >&2
fi

echo "From /manage interface there should be a 'Select Type to Add' and says Plone Site"
echo "The default Plone administrator userid is 'admin' with password 'plone'." >&2

%postun
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{product_dir}/CMFPlone
%{product_dir}/DCWorkflow
%{product_dir}/i18n
