%define name	texinfo
%define version	4.13a
%define release	%mkrel 3

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Tools needed to create Texinfo format documentation files
License:	GPL
Group:		Publishing
URL:		http://www.texinfo.org/
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.lzma
Source1:	info-dir
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.13-test.patch
Patch3:		texinfo-4.13-fix-crash-used-parallel.patch
Patch107:	texinfo-4.13-vikeys-segfault-fix.patch
Patch108:	texinfo-4.13-xz.patch
# backported from cvs
Patch109:	texinfo-4.13-use-size_t-for-len.patch
# Local fixes submitted upstream
Patch200:	texinfo-4.13-mb_modeline.patch
# (anssi 01/2008) for make check:
%if %bootstrap == 0
Requires:	texlive
BuildRequires:	texlive
%endif
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel
BuildRequires:	help2man
Requires(pre):	info-install
Requires(preun):	info-install
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Texinfo is a documentation system that can produce both online information
and printed output from a single source file.  Normally, you'd have to
write two separate documents: one for online help or other online
information and the other for a typeset manual or other printed work.
Using Texinfo, you only need to write one source document.  Then when the
work needs revision, you only have to revise one source document.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you are
going to write documentation for the GNU Project.

%package -n info
Summary:	A stand-alone TTY-based reader for GNU texinfo documentation
Group:		System/Base
Requires(pre):	info-install
Requires(preun):	info-install

%description -n	info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%package -n info-install
Summary:	Program to update the GNU texinfo documentation main page
Group:		System/Base
Requires:	xz
# explicit file provides
Provides:	/sbin/install-info

%description -n	info-install
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

%prep
%setup -qn %name-4.13
%patch1 -p1
%patch2 -p1 -b .test~
%patch3 -p1 -b .parallel~
%patch107 -p1
%patch108 -p1 -b .xz~
%patch109 -p1 -b .size_t~
%patch200 -p1 -b .mb_modeline

%build
%configure2_5x \
	--disable-rpath

%make 
rm -f util/install-info
%make -C util LIBS=%{_libdir}/libz.a

%check
# all tests must pass
make check

%install
rm -rf %{buildroot}

%makeinstall_std
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/info-dir
ln -s ../../..%{_sysconfdir}/info-dir %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/install-info
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmconfig

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post -n info
%_install_info info.info

%preun -n info
%_remove_install_info info.info

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS INTRODUCTION NEWS README TODO
%doc --parents info/README
%{_bindir}/makeinfo
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/texi2dvi.1*                         
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man5/texinfo.5*   
%{_datadir}/texinfo

%files -n info
%defattr(-,root,root)
%{_bindir}/info
%{_infodir}/info.info*
%{_bindir}/infokey

%files -n info-install
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/info-dir
%{_infodir}/dir
/sbin/install-info
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*


%changelog
* Sat Mar 19 2011 Paulo Andrade <pcpa@mandriva.com.br> 4.13a-3mdv2011.0
+ Revision: 647042
- Rebuild with texlive

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 4.13a-2mdv2011.0
+ Revision: 607992
- rebuild

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 4.13a-1mdv2010.1
+ Revision: 526011
- New version 4.13a

* Tue Feb 16 2010 Emmanuel Andry <eandry@mandriva.org> 4.13-7mdv2010.1
+ Revision: 506847
- BR help2man
- add upstream patch to fix crash when texi2dvi is used parallel

* Mon Sep 28 2009 Olivier Blin <oblin@mandriva.com> 4.13-6mdv2010.0
+ Revision: 450385
- add bootstrap flag not to depend on text in early bootstrap
  (from Arnaud Patard)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.13-5mdv2010.0
+ Revision: 427347
- rebuild

* Thu Mar 19 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 4.13-4mdv2009.1
+ Revision: 357607
- patch200: fix display of multibyte modelines

* Wed Feb 18 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.13-3mdv2009.1
+ Revision: 342520
- update dependency on 'lzma' to 'xz'
- use size_t for len (P109 from cvs, fixes bug where ie. default info index
  wouldn't be shown when compiled with -fstack-protector)

* Fri Dec 26 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.13-2mdv2009.1
+ Revision: 319330
- ditch INSTALL from docs as it's of no use for a binary package..
- remove explicit .lzma suffix from man pages
- ditch bzip2 dependency as we no longer use it for compression
- add support for new xz format which obsoletes old lzma format
- regenerate texinfo-*-test.patch

* Wed Dec 10 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.13-1mdv2009.1
+ Revision: 312385
- update to new version 4.13
- rediff patch 107
- fix mixture of tabs and spaces

* Fri Sep 05 2008 Thierry Vignaud <tv@mandriva.org> 4.12-1mdv2009.0
+ Revision: 281249
- adjust (and sort) file list for new man pages
- new release
- remove merged upstream lzma support patch
- new release (upstream now uses lzma)

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 4.11-3mdv2009.0
+ Revision: 225683
- rebuild

* Sat Jan 19 2008 Anssi Hannula <anssi@mandriva.org> 4.11-2mdv2008.1
+ Revision: 155146
- buildrequires tetex-latex for make check
- buildrequires tetex for make check
- require virtual texmf-data instead of tetex

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - do not package big ChangeLog
    - reenable test suite so that we can find out which BR is missing

* Tue Nov 13 2007 Thierry Vignaud <tv@mandriva.org> 4.11-1mdv2008.1
+ Revision: 108472
- temporary disable checks (only failed in iurt)

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new version

* Sat Jul 14 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9-1mdv2008.0
+ Revision: 52026
- spec file clean
- disable rpath
- new version

* Wed Jul 11 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.8-10mdv2008.0
+ Revision: 51129
- add requires on lzma for info-install

* Wed Jul 11 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.8-9mdv2008.0
+ Revision: 51125
- increase buffer size to make lzma match actually work without false positives (P4)
- improve matching on old lzma format (P4)
- disable lzma patch for now due to fugly errors screwing up /etc/info-dir
- fix typo in lzma patch (P4) that broke it
- fix detection of future lzma format in P4

* Sat Jun 09 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.8-8mdv2008.0
+ Revision: 37736
- fix matching of new lzma format (thx Lasse Collins)
- fix lzma patch where matching against old(current) format was broken
- add support for new(future) lzma format

* Thu Jun 07 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.8-7mdv2008.0
+ Revision: 36874
- add lzma support (P4)
- move build check to %%check
- cleanups

* Mon Apr 30 2007 Pixel <pixel@mandriva.com> 4.8-6mdv2008.0
+ Revision: 19546
- explicit file provide /sbin/install-info


* Mon Nov 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 4.8-5mdv2007.0
+ Revision: 83619
- Import texinfo

* Mon Nov 13 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.8-5mdv2007.1
- patch 3: fix for security issue CVE-2006-4810

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.8-4mdv2007.0
- Rebuild

* Thu Jun 15 2006 David Walluck <walluck@mandriva.org> 4.8-3mdv2007.0
- Requires: tetex

* Fri Oct 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 4.8-2mdk
- fix prereq (#17420)

* Thu Feb 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.8-1mdk
- new release
- kill patch 109 (merged upstream)

* Wed Dec 15 2004 Guillaume Rousse <guillomovitch@zarb.org> 4.7-3mdk
- make test robust against environment locales
- spec cleanup

* Fri Jul 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.7-2mdk
- patch 109: fix macros support in texinfo so that groff documentation works

* Fri Jul 02 2004 Giuseppe Ghib� <ghibo@mandrakesoft.com> 4.7-1mdk
- Release: 4.7.
- Rebuilt Patch107.

