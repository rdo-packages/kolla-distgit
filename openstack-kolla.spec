%{!?upstream_version: %global upstream_version %{commit}}
%global upstream_name kolla
%global commit bbeda30a9df9021bf463b90d864e39cd6d7870df
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

Name:       openstack-kolla
Version:    5.0.0
Release:    0.1%{?alphatag}%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://github.com/openstack/%{upstream_name}/archive/%{commit}.tar.gz#/%{upstream_name}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-oslo-config
BuildRequires:  crudini
BuildRequires:  git

Requires:   python-gitdb
Requires:   GitPython
Requires:   python-jinja2 >= 2.8
Requires:   python-docker >= 2.0.0
Requires:   python-six >= 1.9.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-cryptography >= 1.6
Requires:   python-netaddr

%description
Templates and tools from the Kolla project to build OpenStack container images.

%prep
%autosetup -n kolla-%{upstream_version} -S git

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
* Thu Aug 31 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 5.0.0-0.1.bbeda30agit
- Pike update 5.0.0 pre-release (bbeda30a9df9021bf463b90d864e39cd6d7870df)

