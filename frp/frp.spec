%define debug_package %{nil}

Name:           frp
Version:        0.54.0
Release:        2%{?dist}
Summary:        A fast reverse proxy

License:        Apache-2.0
URL:            https://github.com/fatedier/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        frpc.service
Source2:        frps.service

BuildRequires:  systemd-rpm-macros
BuildRequires:  golang
BuildRequires:  git

%description
frp is a fast reverse proxy that allows you to expose a local server located behind a NAT or firewall to the Internet. It currently supports TCP and UDP, as well as HTTP and HTTPS protocols, enabling requests to be forwarded to internal services via domain name.

%prep
%autosetup

%build
export GO111MODULE="on"
export GO_BUILD="CGO_ENABLED=0"
export LDFLAGS="-s -w"
go build -trimpath -ldflags "${LDFLAGS}" -tags frpc -o %{_builddir}/frpc ./cmd/frpc
go build -trimpath -ldflags "${LDFLAGS}" -tags frps -o %{_builddir}/frps ./cmd/frps

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vd                     %{buildroot}%{_unitdir}
install -m 0755 -vd                     %{buildroot}%{_sysconfdir}/%{name}
install -m 0755 -vp %{_builddir}/frpc   %{buildroot}%{_bindir}/
install -m 0755 -vp %{_builddir}/frps   %{buildroot}%{_bindir}/
install -m 0644 -vp %{S:1}              %{buildroot}%{_unitdir}/
install -m 0644 -vp %{S:2}              %{buildroot}%{_unitdir}/
install -m 0644 -v  conf/frpc.toml      %{buildroot}%{_sysconfdir}/%{name}/
install -m 0644 -v  conf/frps.toml      %{buildroot}%{_sysconfdir}/%{name}/

%post
%systemd_post                   frpc.service frps.service

%preun
%systemd_preun                  frpc.service frps.service

%postun
%systemd_postun_with_restart    frpc.service frps.service

%files
%license    LICENSE
%doc        doc README.md README_zh.md Release.md
%config(noreplace) %{_sysconfdir}/%{name}/frpc.toml
%config(noreplace) %{_sysconfdir}/%{name}/frps.toml
%{_bindir}/frpc
%{_bindir}/frps
%{_unitdir}/frpc.service
%{_unitdir}/frps.service

%changelog
%autochangelog
