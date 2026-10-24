Name:		kernel
Version:	5.15.0
Release:	1.els
Summary:	Linux kernel powerpc/irq compiling fix
License:	GPLv2

Source0:	linux-%{version}.tar.xz
Patch0001:	0001-powerpc-irq-Fix-build-with-CONFIG_PROC_FS-n.patch
Patch0002:	0002-hfsplus-fix-uninit-value-in-copy_name.patch

%prep
%setup -q
%patch0001 -p1
%patch0002 -p1

%build
make olddefconfig
make bzImage modules

%install
mkdir -p %{buildroot}/boot
cp arch/x86/boot/bzImage
%{buildroot}/boot/vmlinux-%{version}

%files
/boot/vmlinux-%{version}
