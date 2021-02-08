%global rust_armv7hl_triple armv7-unknown-linux-gnueabihf
%global rust_aarch64_triple aarch64-unknown-linux-gnu
%global rust_x86_triple i686-unknown-linux-gnu

# This sets the type of rpm produced
%define myarch @ARCH@
%define _target_cpu %{myarch}
%define native_triple %{rust_@ARCH@_triple}

# Prevent stripping, python-bytecompiling etc. as this has been already done for the packages
%global __os_install_post %{nil}
# These values would ensure the std-static matched the rustc
# They don't work with tar-git. Leaving the macros in case they're needed one day
%global ver %(rpm -qi rust-std-static-%{rust_x86_triple} | grep Version | cut -f2 -d:)
%global rel %(rpm -qi rust-std-static-%{rust_x86_triple} | grep Release | cut -f2 -d:)

Name:          rust-cross
Version:       1.0+git3
Release:       1
Source10:      precheckin.sh
Source11:      host-gcc-wrapper
# These come from the latest_i486 repo
BuildRequires: rust-std-static-%{rust_x86_triple}
BuildRequires: rust-std-static-%{native_triple}
BuildRequires: fakeroot
# no auto requirements
AutoReqProv:   0
License:        (ASL 2.0 or MIT) and (BSD and MIT)
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
These packages were build by the x86 rust package and imported.

%package -n rust-std-static-%{rust_x86_triple}
# This package is built as an {arch}.rpm and provides the x86 libs
Summary:       Standard library for Rust (%{rust_x86_triple})

%description -n rust-std-static-%{rust_x86_triple}
This is a package providing the rust std static libraries (rlib) for
cross-compiling rust to %{native_triple} in a %{myarch} target.
These packages were build by the x86 rust package and imported.

%prep

%build

%install

#set +x -e
mkdir -p %buildroot
rpm -ql rust-std-static-%{native_triple} > files_for_%{native_triple}
rpm -ql rust-std-static-%{rust_x86_triple} > files_for_%{rust_x86_triple}

cat files_for_%{native_triple} files_for_%{rust_x86_triple} > allfiles

# Copy files to buildroot and preserve permissions.
tar --no-recursion -T allfiles -cpf - | ( cd %buildroot && fakeroot tar -xvpf - ) > filesincluded

mkdir -p %buildroot/usr/lib/rustlib/%{rust_x86_triple}/bin
install -m 755 %{SOURCE11} %buildroot%_libdir/rustlib/%{rust_x86_triple}/bin/%{rust_x86_triple}-gcc

%clean
rm -rf $RPM_BUILD_ROOT

%files -n rust-std-static-%{native_triple}
%defattr(-,root,root)
%dir %{_libdir}
%dir %{_libdir}/rustlib
%{_libdir}/rustlib/%{native_triple}

%files -n rust-std-static-%{rust_x86_triple}
%defattr(-,root,root)
%dir %{_libdir}
%dir %{_libdir}/rustlib
%{_libdir}/rustlib/%{rust_x86_triple}
