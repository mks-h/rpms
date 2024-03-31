%define debug_package %{nil}
%global build_timestamp %(date +"%Y%m%d")

Name:           mihomo
Version:        1.18.3
Release:        %autorelease
Summary:        Another Mihomo Kernel.

License:        GPL-3.0-only
URL:            https://github.com/MetaCubeX/mihomo
Source0:        https://github.com/MetaCubeX/mihomo/archive/refs/tags/v%{version}.tar.gz
Source1:        mihomo.service
Source2:        mihomo@.service

BuildRequires:  systemd-rpm-macros
BuildRequires:  golang
BuildRequires:  git

%description
%{summary}

%prep
%autosetup
chmod -x docs/logo.png

%build
export GO_BUILD="CGO_ENABLED=0"
export LDFLAGS="-X github.com/metacubex/mihomo/constant.Version=%{version} \
                -X github.com/metacubex/mihomo/constant.BuildTime=%{build_timestamp}"
go build -tags with_gvisor -trimpath -ldflags "${LDFLAGS}" -o %{_builddir}/mihomo

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vd                     %{buildroot}%{_userunitdir}
install -m 0755 -vd                     %{buildroot}%{_unitdir}
install -m 0755 -vp %{_builddir}/mihomo %{buildroot}%{_bindir}/
install -m 0644 -vp %{S:1}              %{buildroot}%{_userunitdir}/
install -m 0644 -vp %{S:2}              %{buildroot}%{_unitdir}/

%post
%systemd_user_post mihomo.service
%systemd_post mihomo@.service

%preun
%systemd_user_preun mihomo.service
if [ $1 -eq 0 ] && [ -x /usr/bin/systemctl ] ; then
        /usr/bin/systemctl --no-reload stop mihomo@*.service || :
        /usr/bin/systemctl --no-reload disable mihomo@.service || :
fi
	
%postun
%systemd_user_postun_with_restart mihomo.service
%systemd_postun_with_restart mihomo@*.service

%files
%license LICENSE
%doc docs README.md
%{_bindir}/mihomo
%{_userunitdir}/mihomo.service
%{_unitdir}/mihomo@.service

%changelog
%autochangelog
