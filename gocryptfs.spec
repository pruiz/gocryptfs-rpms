#### NOTE: if building locally you may need to do the following:
####
#### yum install rpmdevtools -y
#### spectool -g -R rpm/gocryptfs.spec
####
#### At this point you can use rpmbuild -ba gocryptfs.spec
#### (this is because our Source0 is a remote Github location


%define _version 1.6.1
%define _release %{lua: print(os.date("%y%m%d"))}

Name:		gocryptfs
Version: 	%{_version}
Release: 	%{_release}%{?dist}
Summary: 	Encrypted overlay filesystem written in Go
URL:     	https://nuetzlich.net/gocryptfs/
License: 	MIT
Source0: 	https://github.com/rfjakob/gocryptfs/releases/download/v%{version}/gocryptfs_v%{version}_linux-static_amd64.tar.gz
Patch0:		8f2723b38-add-nofail.diff
Requires:	fuse
BuildRequires: 	golang
BuildRequires: 	openssl-devel
BuildRequires: 	pandoc
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
gocryptfs uses file-based encryption that is implemented
as a mountable FUSE filesystem. Each file in gocryptfs
is stored one corresponding encrypted file on the hard disk.

%prep
%setup -c %{name}-%{version}
%patch -p0

%install
install -D -m 0755 ./gocryptfs %{buildroot}%{_bindir}/gocryptfs
install -D -m 0644 ./gocryptfs.1 %{buildroot}%{_mandir}/man1/gocryptfs.1

%files
%{_bindir}/gocryptfs
%{_mandir}/man1/*

%changelog
