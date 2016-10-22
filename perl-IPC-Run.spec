%{?scl:%scl_package perl-IPC-Run}

Name:           %{?scl_prefix}perl-IPC-Run
Version:        0.94
Release:        6%{?dist}
Summary:        Perl module for interacting with child processes
# the rest:                     GPL+ or Artistic
# The Win32* modules are not part of the binary RPM package
# lib/IPC/Run/Win32Helper.pm:   GPLv2 or Artistic
# lib/IPC/Run/Win32Pump.pm:     GPLv2 or Artistic
# lib/IPC/Run/Win32IO.pm:       GPLv2 or Artistic
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IPC-Run/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/IPC-Run-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
# IO::Pty not needed strictly for build script
# Run-time:
# base not used on Linux
BuildRequires:  %{?scl_prefix}perl(bytes)
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(Errno)
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(Fcntl)
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(IO::Handle)
BuildRequires:  %{?scl_prefix}perl(IO::Pty) >= 1.08
BuildRequires:  %{?scl_prefix}perl(POSIX)
# Socket not used on Linux
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(Symbol)
# Text::ParseWords not used on Linux
BuildRequires:  %{?scl_prefix}perl(UNIVERSAL)
BuildRequires:  %{?scl_prefix}perl(vars)
# Win32::Process not used on Linux
# Win32API::File not used on Linux
# Tests:
BuildRequires:  %{?scl_prefix}perl(IO::Tty)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.47
BuildRequires:  %{?scl_prefix}perl(warnings)
# Runtime
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(Data::Dumper)
Requires:       %{?scl_prefix}perl(File::Basename)
Requires:       %{?scl_prefix}perl(IO::Pty) >= 1.08

%description
IPC::Run allows you run and interact with child processes using files,
pipes, and pseudo-ttys. Both system()-style and scripted usages are
supported and may be mixed. Likewise, functional and OO API styles are
both supported and may be mixed.

Various redirection operators reminiscent of those seen on common Unix
and DOS command lines are provided.

%prep
%setup -q -n IPC-Run-%{version}

# Remove Windows-only features that could add unnecessary dependencies
rm -f lib/IPC/Run/Win32*
sed -i -e '/^lib\/IPC\/Run\/Win32.*/d' MANIFEST
rm -f t/win32_*
sed -i -e '/^t\/win32_.*/d' MANIFEST

# Fix shellbangs
for file in eg/run_daemon abuse/timers abuse/blocking_debug_with_sub_coprocess ; do
    %{?scl:scl enable %{scl} 'perl -MConfig -pi -e %{?scl:'"}'%{?scl:"'}s,^#!.*/perl,$Config{startperl}}, if ($. == 1)%{?scl:'"}'%{?scl:"'} %{?scl:'}"$file"%{?scl:'}%{?scl:'}
done

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENSE
%doc Changes README TODO
%doc abuse/ eg/
%{perl_vendorlib}/IPC/
%{_mandir}/man3/IPC::Run.3*
%{_mandir}/man3/IPC::Run::Debug.3*
%{_mandir}/man3/IPC::Run::IO.3*
%{_mandir}/man3/IPC::Run::Timer.3*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 0.94-6
- SCL

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.94-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.94-2
- Perl 5.22 rebuild

* Mon Dec 15 2014 Paul Howarth <paul@city-fan.org> - 0.94-1
- Update to 0.94
  - Update License discrepancies (CPAN RT#100858)
  - Many typo corrections
  - Fix t/pty.t fails on Solaris 10 (CPAN RT#20105)
- Drop upstreamed patch for CPAN RT#20105
- Use %%license

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 0.93-1
- 0.93 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.92-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Paul Howarth <paul@city-fan.org> - 0.92-5
- Address intermittent test failures (CPAN RT#20105, RH BZ#1094395)
- Add runtime dependency on Data::Dumper
- Add build dependency on IO::Tty for the test suite
- Make %%files list more explicit

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.92-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Petr Šabata <contyk@redhat.com> - 0.92-1
- 0.92 bump
- Modernize the spec
- Fix dependencies
- Enable the test suite
- Drop command macros

* Thu Sep 13 2012 Petr Pisar <ppisar@redhat.com> - 0.89-9
- IO::Pty is required when passing ">pty>" argument (bug #857030)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.89-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.89-5
- Perl mass rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.89-4
- Perl mass rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.89-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 08 2010 Iain Arnell <iarnell@epo.org> 0.89-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.84-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.84-2
- rebuild against perl 5.10.1

* Wed Sep 02 2009 Steven Pritchard <steve@kspei.com> 0.84-1
- Update to 0.84.
- Drop IPCRUNDEBUG from "make test" (bug fixed long ago).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Steven Pritchard <steve@kspei.com> 0.82-1
- Update to 0.82.
- Use fixperms macro instead of our own chmod incantation.
- Fix Source0 URL.
- BR Test::More.
- Include LICENSE, README, and abuse/ in docs.
- Cleanup to more closely resemble cpanspec output.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.80-5
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.80-4
- rebuild for new perl

* Tue Apr 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.80-3
- BuildRequire perl(ExtUtils::MakeMaker).

* Wed Aug 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.80-2
- Fix order of arguments to find(1).

* Thu May 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.80-1
- 0.80, fine tune build dependencies.

* Tue Jan 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.79-3
- Rebuild, cosmetic cleanups.

* Sun Apr 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.79-2
- Exclude Win32 specific modules.
- Include more docs.
- Skip tests if /dev/pts doesn't exist.

* Sat Apr  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.79-1
- 0.79.

* Sat Apr  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.78-2
- Sync with fedora-rpmdevtools' Perl spec template.
- Improve dependency filtering script.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.78-0.fdr.1
- Update to 0.78.

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.77-0.fdr.4
- Reduce directory ownership bloat.

* Fri Nov 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.77-0.fdr.3
- BuildRequire perl-IO-Tty for better test coverage.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.77-0.fdr.2
- Fix typo in dependency filtering scriptlet.

* Sat Sep 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.77-0.fdr.1
- Update to 0.77.

* Fri Sep  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.75-0.fdr.3
- Avoid Win32-specific dependencies.
- Use PERL_INSTALL_ROOT.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.75-0.fdr.2
- Install into vendor dirs.

* Thu Jun 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.75-0.fdr.1
- First build.
