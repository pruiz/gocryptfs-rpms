#### NOTE: if building locally you may need to do the following:
####
#### yum install rpmdevtools -y
#### spectool -g -R rpm/gocryptfs.spec
####
#### At this point you can use rpmbuild -ba gocryptfs.spec
#### (this is because our Source0 is a remote Github location

%define building_from_source 1

%define _version 1.7
%define _release %{lua: print(os.date("%y%m%d"))}

Name:		gocryptfs
Version: 	%{_version}
Release: 	%{_release}%{?dist}
Summary: 	Encrypted overlay filesystem written in Go
URL:     	https://nuetzlich.net/gocryptfs/
License: 	MIT
Source0:	https://github.com/rfjakob/gocryptfs/releases/download/v%{version}/gocryptfs_v%{version}_src.tar.gz
Patch0:		8f2723b38-add-nofail.diff
Requires:	fuse
%if 0%{building_from_source} > 0
BuildRequires: 	golang
BuildRequires: 	openssl-devel
BuildRequires: 	pandoc
BuildRequires: 	git
%endif
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
gocryptfs uses file-based encryption that is implemented
as a mountable FUSE filesystem. Each file in gocryptfs
is stored one corresponding encrypted file on the hard disk.

%prep
%setup -c %{name}_v%{version}_src
%patch0 -p0

mkdir -p ./_build/src/github.com/rfjakob
ln -s $(pwd) ./_build/src/github.com/rfjakob/gocryptfs

export GOPATH=$(pwd)/_build:%{gopath}
pushd ./_build/src/github.com/rfjakob/gocryptfs
go get -d -t -v ./...
./build.bash
cp _build/bin/gocryptfs .
cp ./Documentation/gocryptfs.1 .
popd

%install
install -D -m 0755 ./gocryptfs %{buildroot}%{_bindir}/gocryptfs
install -D -m 0644 ./gocryptfs.1 %{buildroot}%{_mandir}/man1/gocryptfs.1

%files
%{_bindir}/gocryptfs
%{_mandir}/man1/*

%changelog
