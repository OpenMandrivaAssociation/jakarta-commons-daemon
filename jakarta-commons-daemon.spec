%define native      %{?_with_native:1}%{!?_with_native:0}

%define base_name   daemon
%define short_name  commons-%{base_name}
%define name        jakarta-%{short_name}
%define section     free
%define gcj_support 1

%if %{native}
%define gcj_support 0
%endif

Name:           %{name}
Version:        1.0.1
Release:        %mkrel 4.5
Epoch:          1
Summary:        Jakarta Commons Daemon Package
License:        Apache License
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
URL:            http://jakarta.apache.org/commons/daemon/
Source0:        http://www.apache.org/dist/jakarta/commons/daemon/source/daemon-%{version}.tar.bz2
Patch:          %{name}-crosslink.patch

%if %{native}
BuildRequires:  java-devel
%else
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRequires:  ant, java-javadoc
%endif
BuildRequires:  java-rpmbuild >= 0:1.5
Provides:       %{short_name}
Obsoletes:      %{short_name}

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
chmod 644 src/samples/*


%build
%if %{native}
cd src/native/unix
%configure --with-java=%{java_home}
make %{?_smp_mflags}
%else
%ant -Dant.lib=%{_javadir} -Dj2se.javadoc=%{_javadocdir}/java dist
%endif


%install
rm -rf $RPM_BUILD_ROOT
%if %{native}
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_sbindir}/jsvc
%else
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 dist/%{short_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}


%if %{native}
%files jsvc
%defattr(-,root,root,-)
%doc LICENSE*
%{_sbindir}/jsvc
%else

%files
%defattr(-,root,root,-)
%doc LICENSE* PROPOSAL.html RELEASE-NOTES.txt STATUS.html src/samples
%doc src/docs/*
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%endif


