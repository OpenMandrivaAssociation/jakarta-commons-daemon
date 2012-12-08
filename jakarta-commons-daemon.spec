%define base_name   daemon
%define short_name  commons-%{base_name}
%define name        jakarta-%{short_name}
%define section     free
%define gcj_support 1

Name:           %{name}
Version:        1.0.1
Release:        %mkrel 12
Epoch:          1
Summary:        Jakarta Commons Daemon Package
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://jakarta.apache.org/commons/daemon/
Source0:        http://www.apache.org/dist/jakarta/commons/daemon/source/daemon-%{version}.tar.bz2
Patch0:          %{name}-crosslink.patch
Patch1:		 daemon-1.0.1-asneeded.patch

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRequires:  ant, java-javadoc
BuildRequires:  java-rpmbuild >= 0:1.5
Provides:       %{short_name}
Obsoletes:      %{short_name}
ExcludeArch:	%arm %mips

%description
The scope of this package is to define an API in line with the current
Java(tm) Platform APIs to support an alternative invocation mechanism
which could be used instead of the above mentioned public static void
main(String[]) method.  This specification cover the behavior and life
cycle of what we define as Java(tm) daemons, or, in other words, non
interactive Java(tm) applications.

%package        jsvc
Summary:        Java daemon launcher
Group:          Development/Java
Provides:       jsvc = %{epoch}:%{version}-%{release}

%description    jsvc
%{summary}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{base_name}-%{version}
%patch0 -p0
%patch1 -p1 -b .asneeded
chmod 644 src/samples/*


%build
pushd src/native/unix
%configure --with-java=%{java_home}
make %{?_smp_mflags}
popd
%ant -Dant.lib=%{_javadir} -Dj2se.javadoc=%{_javadocdir}/java dist

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_sbindir}/jsvc
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 dist/%{short_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files jsvc
%defattr(-,root,root,-)
%doc LICENSE*
%{_sbindir}/jsvc

%files
%defattr(-,root,root,-)
%doc LICENSE* PROPOSAL.html RELEASE-NOTES.txt STATUS.html src/samples
%doc src/docs/*
%{_javadir}/*
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-11mdv2011.0
+ Revision: 665799
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-10mdv2011.0
+ Revision: 606050
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-9mdv2010.1
+ Revision: 522965
- rebuilt for 2010.1

* Fri Sep 25 2009 Olivier Blin <oblin@mandriva.com> 1:1.0.1-8mdv2010.0
+ Revision: 449220
- fix build with --as-needed linker flag
- do not build on mips & arm (from Arnaud Patard)
- fix patch declaration (from Arnaud Patard)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Feb 19 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1:1.0.1-6.0.1mdv2008.1
+ Revision: 173063
- enable jsvc

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 1:1.0.1-4.5mdv2008.1
+ Revision: 127268
- kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:1.0.1-4.4mdv2008.0
+ Revision: 87403
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 1:1.0.1-4.3mdv2008.0
+ Revision: 82678
- update to new version


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0.1-4.2mdv2007.1
+ Revision: 143905
- rebuild for 2007.1
- Import jakarta-commons-daemon

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 1:1.0.1-4.1mdv2007.0
- bump release

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 1:1.0.1-1mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 1:1.0-2.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 1:1.0-2jpp
- Rebuild with ant-1.6.2

* Wed May 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-1jpp
- Update to 1.0.

