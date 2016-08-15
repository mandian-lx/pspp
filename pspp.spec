#define _disable_ld_no_undefined 1

Summary:	A program for statistical analysis of sampled data
Name:		pspp
Version:	0.10.2
Release:	1
License:	GPLv3+
Group:		Sciences/Mathematics
URL:		https://www.gnu.org/software/pspp/
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	httsp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:	perl
BuildRequires:	perl-devel
BuildRequires:	postgresql-server # test propouse only
BuildRequires:	readline-devel
BuildRequires:	texinfo
#BuildRequires:	texlive
BuildRequires:	perl(ExtUtils::Constant)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Text::Diff)
BuildRequires:	perl(Test::More)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(zlib)

Suggests:	yelp

%description
PSPP is a program for statistical analysis of sampled data. It is
a free replacement for the proprietary program SPSS.

PSPP supports T-tests, ANOVA and GLM analyses, factor analysis,
non-parametric tests, linear and logistic regression, clustering,
and other statistical features.	PSPP produces statistical reports in
plain text, PDF, PostScript, CSV, HTML, SVG, and OpenDocument formats.
It can import data from OpenDocument, Gnumeric, text and SPSS formats.

PSPP has both text-based and graphical user interfaces.	The PSPP
user interface has been translated into a number of languages.

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}ire
%{_bindir}/%{name}-convert
%{_bindir}/%{name}-dump-sav
%{_libdir}/%{name}/lib%{name}-%{version}.so
%{_libdir}/%{name}/lib%{name}-core-%{version}.so
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/apps/pspp.svg
%{_datadir}/%{name}/
%{_infodir}/%{name}*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}ire.1*
%{_mandir}/man1/%{name}-convert.1*
%{_mandir}/man1/%{name}-dump-sav.1*
%doc README
%doc NEWS
%doc ONEWS
%doc ChangeLog
%doc TODO
%doc AUTHORS
%doc THANKS
%doc COPYING

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for PSPP
Group:		Development/C

%description devel
Development files for developping applications that require PSPP.

%files devel
%{_libdir}/%{name}/lib%{name}.so
%{_libdir}/%{name}/lib%{name}-core.so
%doc ChangeLog
%doc TODO
%doc AUTHORS
%doc THANKS
%doc COPYING

#----------------------------------------------------------------------------

%prep
%setup -q

# fix file-not-utf8 warning
for f in ChangeLog
do
	iconv -f iso8859-1 -t utf8 ${f} > ${f}.tmp
	touch -r ${f} ${f}.tmp
	mv -f ${f}.tmp ${f}
done

%build
autoreconf -ifv
%configure
%make all doc

%install
%make_install

# don't lala
find %{buildroot}%{_libdir} -name \*.la -delete

# localization
%find_lang %{name}

%check
%make check || true

# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/pspp.desktop

