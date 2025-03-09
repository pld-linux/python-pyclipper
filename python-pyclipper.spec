#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Cython wrapper for Clipper library
Summary(pl.UTF-8):	Cythonowe obudowanie biblioteki Clipper
Name:		python-pyclipper
Version:	1.3.0.post2
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyclipper/
Source0:	https://files.pythonhosted.org/packages/source/p/pyclipper/pyclipper-%{version}.tar.gz
# Source0-md5:	ac53748592d18d8c8b63b5bd65a2ab28
Patch0:		%{name}-tests.patch
URL:		https://pypi.org/project/pyclipper/
BuildRequires:	libstdc++-devel
%if %{with python2}
BuildRequires:	python-Cython >= 0.28
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.11.1
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.28
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.11.1
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyclipper is a Cython wrapper exposing public functions and classes of
the C++ translation of the Angus Johnson's Clipper library.

The Clipper library performs line & polygon clipping - intersection,
union, difference & exclusive-or, and line & polygon offsetting. The
library is based on Vatti's clipping algorithm.

%description -l pl.UTF-8
Pyclipper to cythonowe obudowanie udostępniające funkcje i klasy
publiczne tłumaczenia C++ biblioteki Clipper Angusa Johnsona.

Biblioteka Clipper wykonuje obcinanie linii i wielokątów (wyznaczanie
części wspólnej, sumy, różnicy i różnicy symetrycznej) oraz
obrysowywanie linii i wielokątów. Jest oparta na algorytmie obcinania
Vattiego.

%package -n python3-pyclipper
Summary:	Cython wrapper for Clipper library
Summary(pl.UTF-8):	Cythonowe obudowanie biblioteki Clipper
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pyclipper
Pyclipper is a Cython wrapper exposing public functions and classes of
the C++ translation of the Angus Johnson's Clipper library.

%description -n python3-pyclipper -l pl.UTF-8
Pyclipper to cythonowe obudowanie udostępniające funkcje i klasy
publiczne tłumaczenia C++ biblioteki Clipper Angusa Johnsona.

Biblioteka Clipper wykonuje obcinanie linii i wielokątów (wyznaczanie
części wspólnej, sumy, różnicy i różnicy symetrycznej) oraz
obrysowywanie linii i wielokątów. Jest oparta na algorytmie obcinania
Vattiego.

%prep
%setup -q -n pyclipper-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/pyclipper
%{py_sitedir}/pyclipper/*.py[co]
%attr(755,root,root) %{py_sitedir}/pyclipper/*.so
%{py_sitedir}/pyclipper-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pyclipper
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/pyclipper
%{py3_sitedir}/pyclipper/*.py
%attr(755,root,root) %{py3_sitedir}/pyclipper/*.so
%{py3_sitedir}/pyclipper/__pycache__
%{py3_sitedir}/pyclipper-%{version}-py*.egg-info
%endif
