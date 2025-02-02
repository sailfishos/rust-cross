%global rust_armv7hl_triple armv7-unknown-linux-gnueabihf
%global rust_aarch64_triple aarch64-unknown-linux-gnu

# Host triple
%ifarch %ix86
%global rust_host_triple i686-unknown-linux-gnu
%global rust_host_arch x86
%else
%global rust_host_triple x86_64-unknown-linux-gnu
%global rust_host_arch x86_64
%endif

# This sets the type of rpm produced
%define myarch @ARCH@
%define _target_cpu %{myarch}
%define native_triple %{rust_@ARCH@_triple}

# Prevent stripping, python-bytecompiling etc. as this has been already done for the packages
%global __os_install_post %{nil}
# These values would ensure the std-static matched the rustc
# They don't work with tar-git. Leaving the macros in case they're needed one day
%global ver %(rpm -qi rust-std-static-%{rust_host_triple} | grep Version | cut -f2 -d:)
%global rel %(rpm -qi rust-std-static-%{rust_host_triple} | grep Release | cut -f2 -d:)

Name:          rust-cross
Version:       1.0+git4
Release:       1
Source10:      precheckin.sh
Source11:      host-gcc-wrapper
# These come from the latest_i486 or latest_x86_64 repo
BuildRequires: rust-std-static-%{rust_host_triple}
BuildRequires: rust-std-static-%{native_triple}
BuildRequires: fakeroot
# no auto requirements
AutoReqProv:   0
License:       (ASL 2.0 or MIT) and (BSD and MIT)
Summary:       Standard library for Rust
%description
The main package isn't built


%package -n rust-std-static-%{native_triple}
# This package is built as an {arch}.rpm and provides the native libs
# So it also provides the default std-static libraries
Provides: rust-std-static
Summary:       Standard library for Rust (%{native_triple})

%description -n rust-std-static-%{native_triple}

This is a package providing the rust std static libraries (rlib) for
compiling rust for an %{myarch} target.
These packages were build by the %{rust_host_arch} rust package and imported.

%package -n rust-std-static-%{rust_host_triple}
# This package is built as an {arch}.rpm and provides the %{rust_host_arch} libs
Summary:       Standard library for Rust (%{rust_host_triple})

%description -n rust-std-static-%{rust_host_triple}
This is a package providing the rust std static libraries (rlib) for
cross-compiling rust to %{native_triple} in a %{myarch} target.
These packages were build by the %{rust_host_arch} rust package and imported.

%prep

%build

%install

#set +x -e
mkdir -p %buildroot
rpm -ql rust-std-static-%{native_triple} > files_for_%{native_triple}
rpm -ql rust-std-static-%{rust_host_triple} > files_for_%{rust_host_triple}

cat files_for_%{native_triple} files_for_%{rust_host_triple} > allfiles

# Copy files to buildroot and preserve permissions.
tar --no-recursion -T allfiles -cpf - | ( cd %buildroot && fakeroot tar -xvpf - ) > filesincluded

mkdir -p %buildroot%{_prefix}/lib/rustlib/%{rust_host_triple}/bin
install -m 755 %{SOURCE11} %buildroot%{_prefix}/lib/rustlib/%{rust_host_triple}/bin/%{rust_host_triple}-gcc

%files -n rust-std-static-%{native_triple}
%dir %{_prefix}/lib
%dir %{_prefix}/lib/rustlib
%{_prefix}/lib/rustlib/%{native_triple}

%files -n rust-std-static-%{rust_host_triple}
%dir %{_prefix}/lib
%dir %{_prefix}/lib/rustlib
%{_prefix}/lib/rustlib/%{rust_host_triple}
