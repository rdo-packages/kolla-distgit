%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Templates and tools from the Kolla project to build OpenStack container images.

Name:       openstack-kolla
Version:    16.0.0
Release:    0.1%{?milestone}%{?dist}
Summary:    Build OpenStack container images

License:    ASL 2.0
URL:        http://pypi.python.org/pypi/kolla
Source0:    https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz
#
# patches_base=16.0.0.0rc1
#

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/kolla/kolla-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-oslo-config
BuildRequires:  crudini

Requires:   python3-pbr >= 2.0.0
Requires:   python3-jinja2 >= 3.0.1
Requires:   python3-docker >= 3.0.0
Requires:   python3-oslo-config >= 2:5.1.0

Requires:   python3-GitPython >= 1.0.1

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
* Fri May 26 2023 RDO <dev@lists.rdoproject.org> 16.0.0-0.1.0rc1
- Update to 16.0.0.0rc1

