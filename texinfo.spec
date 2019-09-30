%global tex_texinfo %{_datadir}/texmf/tex/texinfo

Name: texinfo
Version: 6.5
Release: 13
Summary: Tools needed to create Texinfo format documentation files
License: GPLv3+
Url: http://www.gnu.org/software/texinfo/
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz.sig

Patch0: texinfo-4.12-zlib.patch
# Patch1: this is needed just for koji/mock, all tests pass fine in local build
Patch1: texinfo-6.0-disable-failing-info-test.patch
# Patch2: rhbz#1348671, because of OSTree
Patch2: texinfo-6.1-install-info-use-create-tmp-then-rename-pattern.patch
# Patch3: we need to fix template fix-info-dir generates
Patch3: info-6.5-sync-fix-info-dir.patch
# Update to 2018-03-10 texinfo.tex
Patch4: texinfo-20180310-texinfo.tex.patch
# rhbz#1592433, bug in fix-info-dir --delete
Patch5: texinfo-6.5-fix-info-dir.patch
# Patch6: rhbz#1590308, fixes test fail with unescaped left brace
Patch6: texinfo-6.5-fix-for-perl-5.28.patch
# Patch7: fixes issues detected by static analysis
Patch7: texinfo-6.5-covscan-fixes.patch

Patch6000:  fix-misleading-warning-about-node-names.patch
Patch6001:  perl-5.28-thread-safe-locales.patch
Patch6002:  MiscXS-avoid-memory-leak.patch
Patch6003:  XS-avoid-memory-leak.patch
Patch6004:  XS-avoid-memory-leaks.patch
Patch6005:  Fix-call-to-info_find_file.patch
Patch6006:  Avoid-memory-leak-for-malformed-files.patch
Patch6007:  Fix-day-one-bug-handling-as-command-character.patch

BuildRequires: gcc perl-generators zlib-devel ncurses-devel help2man
BuildRequires: perl(Data::Dumper) perl(Locale::Messages) perl(Unicode::EastAsianWidth) perl(Text::Unidecode) perl(Storable)

# Texinfo perl packages are not installed in default perl library dirs
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package tex
Summary: Tools for formatting Texinfo documentation files using TeX
Requires: texinfo = %{version}-%{release} tex(tex) tex(epsf.tex)
Requires(post): texlive-tetex
Requires(postun): texlive-tetex

%description tex
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package  help
Summary: A stand-alone TTY-based reader for GNU texinfo documentation

%description  help
The GNU project uses the texinfo file format for much of its
documentation. The help package provides a standalone TTY-based
browser program for viewing texinfo files.

%prep
%autosetup -p1

%build
%configure --with-external-Text-Unidecode --with-external-libintl-perl --with-external-Unicode-EastAsianWidth --disable-perl-xs
%make_build

%install
mkdir -p ${RPM_BUILD_ROOT}/sbin

%make_install

mkdir -p $RPM_BUILD_ROOT%{tex_texinfo}
install -p -m644 doc/texinfo.tex doc/txi-??.tex $RPM_BUILD_ROOT%{tex_texinfo}

mv $RPM_BUILD_ROOT%{_bindir}/install-info $RPM_BUILD_ROOT/sbin

install -Dpm0755 -t %{buildroot}%{_sbindir} contrib/fix-info-dir

%find_lang %{name}
%find_lang %{name}_document

%check
export ALL_TESTS=yes
%make_build check

%post 
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun 
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%transfiletriggerin help -- %{_infodir}
[ -f %{_infodir}/dir ] && create_arg="" || create_arg="--create"
%{_sbindir}/fix-info-dir $create_arg %{_infodir}/dir &>/dev/null

%transfiletriggerpostun help -- %{_infodir}
[ -f %{_infodir}/dir ] && %{_sbindir}/fix-info-dir --delete %{_infodir}/dir &>/dev/null

%files -f %{name}.lang -f %{name}_document.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo

%files tex
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi

%files -n info
%license COPYING
%{_bindir}/info
/sbin/install-info
%{_sbindir}/fix-info-dir

%files help
%license COPYING
%{_infodir}/info-stnd.info*
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
%{tex_texinfo}/
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/texinfo.5* 
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*
%{_infodir}/texinfo*
%ghost %{_infodir}/dir
%ghost %{_infodir}/dir.old

%changelog
* Wed Sep 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-13
- Add rpm texinfo-tex, info 

* Tue Sep 17 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-12
- Package init
