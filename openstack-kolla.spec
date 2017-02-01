%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:       openstack-kolla
Version:    XXX
Release:    XXX
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    http://tarballs.openstack.org/kolla/kolla-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python2-oslo-config

Requires:   python-setuptools
Requires:   python-gitdb
Requires:   GitPython
Requires:   python-jinja2
Requires:   python-docker-py
Requires:   python-six
Requires:   python2-oslo-config
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
%{_datadir}/kolla/docker
%{_datadir}/kolla/setup.cfg
%{_sysconfdir}/kolla/*

%changelog
