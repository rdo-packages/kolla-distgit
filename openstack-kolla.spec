%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Templates and tools from the Kolla project to build OpenStack container images.

Name:       openstack-kolla
Version:    7.0.4
Release:    1%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz

#

BuildArch:  noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-oslo-config
BuildRequires:  crudini

Requires:   python-gitdb
Requires:   python2-pbr >= 2.0.0
Requires:   GitPython
Requires:   python2-jinja2 >= 2.8
Requires:   python2-docker >= 2.4.2
Requires:   python2-six >= 1.10.0
Requires:   python2-oslo-config >= 2:5.1.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-cryptography >= 1.9
Requires:   python2-netaddr

%description
%{common_desc}

%prep
%setup -q -n kolla-%{upstream_version}

%build
PYTHONPATH=. oslo-config-generator --config-file=etc/oslo-config-generator/kolla-build.conf

%py2_build

%install
%py2_install

mkdir -p %{buildroot}%{_datadir}/kolla/docker
cp -vr docker/ %{buildroot}%{_datadir}/kolla

# setup.cfg required for kolla-build to discover the version
install -p -D -m 644 setup.cfg %{buildroot}%{_datadir}/kolla/setup.cfg

# remove tests
rm -fr %{buildroot}%{python2_sitelib}/kolla/tests

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
%{python2_sitelib}/kolla*
%{_datadir}/kolla
%{_sysconfdir}/kolla

%changelog
* Mon Sep 09 2019 RDO <dev@lists.rdoproject.org> 7.0.4-1
- Update to 7.0.4

* Fri Jun 14 2019 RDO <dev@lists.rdoproject.org> 7.0.3-1
- Update to 7.0.3

* Thu Apr 11 2019 RDO <dev@lists.rdoproject.org> 7.0.2-1
- Update to 7.0.2

* Mon Jan 07 2019 RDO <dev@lists.rdoproject.org> 7.0.1-1
- Update to 7.0.1

* Tue Oct 23 2018 RDO <dev@lists.rdoproject.org> 7.0.0-1
- Update to 7.0.0

* Mon Oct 22 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.3.0rc2
- Update to 7.0.0.0rc3

* Tue Oct 02 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.2.0rc1
- Update to 7.0.0.0rc2

* Wed Sep 05 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.1.0rc1
- Update to 7.0.0.0rc1

