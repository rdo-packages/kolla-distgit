%global milestone .0rc1
# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Templates and tools from the Kolla project to build OpenStack container images.

Name:       openstack-kolla
Version:    8.0.0
Release:    0.1%{?milestone}%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz

#
# patches_base=8.0.0.0rc1
#

BuildArch:  noarch
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  crudini

Requires:   python%{pyver}-pbr >= 2.0.0
Requires:   python%{pyver}-jinja2 >= 2.8
Requires:   python%{pyver}-docker >= 2.4.2
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-oslo-config >= 2:5.1.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-cryptography >= 1.9
Requires:   python%{pyver}-netaddr

# Handle python2 exception
%if %{pyver} == 2
Requires:   python-gitdb
Requires:   GitPython
%else
Requires:   python%{pyver}-gitdb
Requires:   python%{pyver}-GitPython
%endif

%description
%{common_desc}

%prep
%setup -q -n kolla-%{upstream_version}

%build
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=etc/oslo-config-generator/kolla-build.conf

%{pyver_build}

%install
%{pyver_install}

mkdir -p %{buildroot}%{_datadir}/kolla/docker
cp -vr docker/ %{buildroot}%{_datadir}/kolla

# setup.cfg required for kolla-build to discover the version
install -p -D -m 644 setup.cfg %{buildroot}%{_datadir}/kolla/setup.cfg

# remove tests
rm -fr %{buildroot}%{pyver_sitelib}/kolla/tests

# remove tools
rm -fr %{buildroot}%{_datadir}/kolla/tools

install -d -m 755 %{buildroot}%{_sysconfdir}/kolla
crudini --set %{buildroot}%{_datadir}/kolla/etc_examples/kolla/kolla-build.conf DEFAULT tag %{version}-%{release}
cp -v %{buildroot}%{_datadir}/kolla/etc_examples/kolla/kolla-build.conf %{buildroot}%{_sysconfdir}/kolla
rm -fr %{buildroot}%{_datadir}/kolla/etc_examples

%files
%doc README.rst
%doc %{_datadir}/kolla/doc
%license LICENSE
%{_bindir}/kolla-build
%{pyver_sitelib}/kolla*
%{_datadir}/kolla
%{_sysconfdir}/kolla

%changelog
* Mon Apr 08 2019 RDO <dev@lists.rdoproject.org> 8.0.0-0.1.0rc1
- Update to 8.0.0.0rc1

