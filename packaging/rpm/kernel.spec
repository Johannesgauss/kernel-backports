Name:		kernel
Version:	5.15.0
Release:	1.els
Summary:	Linux kernel powerpc/irq compiling fix
License:	GPLv2

Source0:	linux-%{version}.tar.xz
Patch001:	0001-powerpc-irq-Fix-build-with-CONFIG_PROC_FS-n.Patch001

%prep
%setup -q
%patch001 -p1

%build
make olddefconfig
make bzImage modules

%install
mkdir -p %{buildroot}/boot
cp arch/x86/boot/bzImage
%{buildroot}/boot/vmlinux-%{version}

%files
/boot/vmlinux-%{version}
