%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Templates and tools from the Kolla project to build OpenStack container images.

Name:       openstack-kolla
Version:    10.3.0
Release:    1%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz


BuildArch:  noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-oslo-config
BuildRequires:  crudini

Requires:   python3-pbr >= 2.0.0
Requires:   python3-jinja2 >= 2.8
Requires:   python3-docker >= 2.4.2
Requires:   python3-oslo-config >= 2:5.1.0

Requires:   python3-GitPython

%description
%{common_desc}

%prep
%setup -q -n kolla-%{upstream_version}

%build
PYTHONPATH=. oslo-config-generator --config-file=etc/oslo-config-generator/kolla-build.conf

%{py3_build}

%install
%{py3_install}

mkdir -p %{buildroot}%{_datadir}/kolla/docker
cp -vr docker/ %{buildroot}%{_datadir}/kolla

# setup.cfg required for kolla-build to discover the version
install -p -D -m 644 setup.cfg %{buildroot}%{_datadir}/kolla/setup.cfg

# remove tests
rm -fr %{buildroot}%{python3_sitelib}/kolla/tests

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
%{python3_sitelib}/kolla*
%{_datadir}/kolla
%{_sysconfdir}/kolla


%changelog
* Thu Jul 29 2021 RDO <dev@lists.rdoproject.org> 10.3.0-1
- Update to 10.3.0

* Thu Jan 07 2021 RDO <dev@lists.rdoproject.org> 10.2.0-1
- Update to 10.2.0

* Tue Jul 14 2020 RDO <dev@lists.rdoproject.org> 10.1.0-1
- Update to 10.1.0

* Mon Jun 22 2020 RDO <dev@lists.rdoproject.org> 10.0.0-0.2.0rc1
- Update to 10.0.0.0rc2

* Fri May 22 2020 RDO <dev@lists.rdoproject.org> 10.0.0-0.1.0rc1
- Update to 10.0.0.0rc1

# REMOVEME: error caused by commit https://opendev.org/openstack/kolla/commit/3af23da7ccd07ace68ae5ec6a76b110783fac627
