%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:       openstack-kolla
Version:    4.0.4
Release:    1%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz


BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-oslo-config

Requires:   python-setuptools
Requires:   python-gitdb
Requires:   GitPython
Requires:   python-jinja2
Requires:   python-docker-py
Requires:   python-six
Requires:   python-oslo-config >= 2:3.14.0
Requires:   python-oslo-utils >= 3.18.0
Requires:   python-crypto
Requires:   python-netaddr

%description
Templates and tools from the Kolla project to build OpenStack container images.

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
* Mon Apr 02 2018 RDO <dev@lists.rdoproject.org> 4.0.4-1
- Update to 4.0.4

* Fri Dec 15 2017 RDO <dev@lists.rdoproject.org> 4.0.3-1
- Update to 4.0.3

* Mon Jun 19 2017 rdo-trunk <javier.pena@redhat.com> 4.0.2-1
- Update to 4.0.2

* Thu Apr 20 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.1-1
- Update to 4.0.1

* Tue Mar 14 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-1
- Update to 4.0.0

* Thu Mar 09 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-0.2.0rc2
- Update to 4.0.0.0rc2

* Fri Feb 17 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-0.1.0rc1
- Update to 4.0.0.0rc1

