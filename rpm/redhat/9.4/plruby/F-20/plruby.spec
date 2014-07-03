%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname plruby

%if 0%{?rhel} <= 5
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ' 2>/dev/null)}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %ruby_sitearch}
%else
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"] ' 2>/dev/null)}
%endif

Summary:	PostgreSQL Ruby Procedural Language
Name:		%{sname}%{pgmajorversion}
Version:	0.5.4
Release:	4%{?dist}
Source0:	https://github.com/knu/postgresql-%{sname}/archive/v%{version}/postgresql-%{sname}-%{version}.tar.gz
License:	Ruby or GPL+
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		https://github.com/knu/postgresql-plruby
BuildRequires:	ruby >= 1.8 ruby-devel >= 1.8 postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-libs, ruby(release)

Patch0:		plruby-bitopers.patch
Patch2:		plruby-retval.patch
Patch3:		plruby-includes.patch
Patch4:		plruby-version.patch

%description
PL/Ruby is a loadable procedural language for the PostgreSQL database
system that enable the Ruby language to create functions and trigger 
procedures.

%package doc
Summary:	Documentation for plruby
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for plruby.

%prep
%setup -q -n postgresql-%{sname}-%{version}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%patch0 -p1 -b .biopers
%endif
%patch2 -p1 -b .retval
%patch3 -p1 -b .debug
%patch4 -p1 -b .version

%build
# Using safe-level=3, since Ruby 2.1+ and later does not support safe level
# bigger than 3.
# https://bugs.ruby-lang.org/issues/8468
# https://bugs.ruby-lang.org/projects/ruby-trunk/repository/revisions/41259
# Upstream report: https://github.com/knu/postgresql-plruby/issues/9
ruby extconf.rb --vendor --with-safe-level=3 --with-pg-config=%{pginstdir}/bin/pg_config --with-suffix=%{pgmajorversion}
make

%install
rm -rf %{buildroot}
# ruby_headers= applied as workaround for rhbz#921650.
make DESTDIR=%{buildroot} %{?_smp_mflags} ruby_headers= install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README.en plruby.html 
%dir %{ruby_vendorarchdir}/plruby
%{ruby_vendorarchdir}/plruby/plruby_*.so
%{ruby_vendorarchdir}/plruby%{pgmajorversion}.so

%files doc
%defattr(-,root,root,-)
%doc docs/plruby.rb

%changelog
* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.5.4-4
- Sync with Fedora spec file
- Trim changelog
