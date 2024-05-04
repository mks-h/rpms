FROM docker.io/oraclelinux:9
RUN dnf install rpmdevtools rpm-build
RUN rpmdev-setuptree

WORKDIR /root/rpmbuild

ADD ./frp/frp.spec SPECS
RUN dnf builddep --spec SPECS/frp.spec

RUN dnf remove golang
RUN rm -rf /usr/local/go
ARG BUILDARCH
ADD https://go.dev/dl/go1.22.2.linux-$BUILDARCH.tar.gz /root/
RUN tar -C /usr/local -xzf /root/go1.22.2.linux-$BUILDARCH.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

RUN spectool -gR SPECS/frp.spec
ADD ./frp/frp?.service SOURCES
ENTRYPOINT rpmbuild -ba --nodeps SPECS/frp.spec
VOLUME /root/rpmbuild/RPMS /root/rpmbuild/SRPMS
