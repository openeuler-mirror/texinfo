%global tex_texinfo %{_datadir}/texmf/tex/texinfo
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$

Name: texinfo
Version: 6.8
Release: 2
Summary: The GNU Documentation System
License: GPLv3+
Url: http://www.gnu.org/software/texinfo/
Source0: https://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz.sig

Patch0001: texinfo-6.0-disable-failing-info-test.patch
Patch0002: texinfo-6.1-install-info-use-create-tmp-then-rename-pattern.patch
Patch0003: info-6.5-sync-fix-info-dir.patch
Patch0004: texinfo-6.5-fix-info-dir.patch
Patch0005: texinfo-6.5-covscan-fixes.patch
Patch0006: texinfo-6.8-undo-gnulib-nonnul.patch

BuildRequires: gcc perl-generators zlib-devel ncurses-devel help2man
BuildRequires: perl(Data::Dumper) perl(Locale::Messages) perl(Unicode::EastAsianWidth) perl(Text::Unidecode) perl(Storable) perl(Unicode::Normalize)

%description
Texinfo is a documentation system that uses a single source file to produce
both online information and printed output. Instead of writing different documents
for online presentation and another for printed work, you need have only one document.

Texinfo can produce output in plain ASCII, HTML, its own hypertext format called Info,
and (using TeX) DVI format. It includes the makeinfo program.

%package tex
Summary: Tools for formatting Texinfo documents
Requires: texinfo = %{version}-%{release} tex(tex) tex(epsf.tex)
Requires(post): texlive-tetex
Requires(postun): texlive-tetex
Provides: tex-texinfo = %{version}-%{release}
Obsoletes: tex-texinfo < %{version}-%{release}
Provides: texlive-texinfo > 9:2019-15
Obsoletes: texlive-texinfo <= 9:2019-15

%description tex
This package provides tools for format most of the documents
which produced by texinfo documentation system.

%package -n info
Summary: TTY-based reader of the GNU texinfo documentation

%description -n info
This package provides a standalone TTY-based browser program for viewing texinfo files.

%package  help
Summary: Documentation for texinfo

%description  help
This package contains help documentation for texinfo.

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
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_datadir}/texinfo

%files tex
%{tex_texinfo}/
%{_bindir}/pdftexi2dvi
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf

%files -n info
%license COPYING
%{_bindir}/info
%{_sbindir}/fix-info-dir
/sbin/install-info
%ghost %{_infodir}/dir
%ghost %{_infodir}/dir.old

%files help
%license COPYING
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/pod2texi.1*
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man5/info.5*
%{_mandir}/man5/texinfo.5*

%changelog
* Fri Feb 18 2022 yangcheng <yangcheng87@h-partners.com> - 6.8-2
- Move files to info subpackage to solve uninstall error

* Sat Dec 04 2021 wuchaochao <wuchaochao4@huawei.com> - 6.8-1
- update version to 6.8

* Wed Dec 16 2020 zhanzhimin <zhanzhimin@huawei.com> - 6.7-2
- Update Source0

* Fri Jul 17 2020 chengguipeng <chengguipeng1@huawei.com> - 6.7-1
- upgrade to 6.7-1

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 6.6-2
- update to 6.6-2

* Tue Oct 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-17
- Move tex_texinfo from help to tex package

* Sat Oct 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-16
- Adjust the format and description

* Fri Oct 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-15
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: Restore previous version of 6.5-13

* Mon Oct 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-14
- remove rpm texinfo-tex, info

* Wed Sep 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-13
- Add rpm texinfo-tex, info

* Tue Sep 17 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.5-12
- Package init
