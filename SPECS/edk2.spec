%global edk2_date 20180522
%global edk2_githash 4b8552d

Name: edk2
Summary: EFI Development Kit II
Version: %{edk2_date}git%{edk2_githash}
Release: 1.3.2%{?dist}

License: BSD and MIT
URL: https://github.com/tianocore/edk2

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/edk2/archive?at=4b8552d&format=tar.gz&prefix=edk2-20180522git4b8552d#/edk2-20180522git4b8552d.tar.gz

Patch0: 0001-OvmfPkg-XenSupport-remove-usage-of-prefetchable-PCI-.patch
Patch1: 0002-OvmfPkg-XenSupport-use-a-correct-PCI-host-bridge-ape.patch
Patch2: 0003-OvmfPkg-XenSupport-turn-off-address-decoding-before-.patch
Patch3: nvidia-vgpu-support.patch
Patch4: gvt-g-support.patch
Patch5: set-default-resolution-1024-768.patch
Patch6: embed-nic-drivers.patch
Patch7: add-xen-variable.patch
Patch8: add-xen-platform-device-id.patch
Patch9: disable-modules.patch
Patch10: xenorder.patch
Patch11: keep-caching-enabled.patch
Patch12: ca-306943__disable_pv_drivers_and_reenable_emulated_devices.patch
Patch13: remove_cryptopkg_dependency.patch

Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/edk2.pg/archive?at=1.3.2&format=tar#/edk2.pg.tar) = 1c9d85d847710658ce1eea844764991eed2fe36e
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/edk2/archive?at=4b8552d&format=tar.gz&prefix=edk2-20180522git4b8552d#/edk2-20180522git4b8552d.tar.gz) = 4b8552d794e7b17a6627e0f752fd298e8bcb2587


BuildRequires: gcc gcc-c++
BuildRequires: python
BuildRequires: libuuid-devel
BuildRequires: nasm
BuildRequires: iasl
BuildRequires: ipxe-efi


%description
Provides the Open Virtual Machine Firmware (OVMF) built for x64.
This is a build of the EFI Development Kit II suitable for using
as firmware in a virtual machine.


%prep
%autosetup -p1


%build
cp %{_datadir}/ipxe/10ec8139.efi .
cp %{_datadir}/ipxe/8086100e.efi .

OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=FALSE \
    -D NETWORK_IP6_ENABLE=FALSE \
    -D IPXE_ENABLE=TRUE \
    -D HTTP_BOOT_ENABLE=FALSE \
    -D TLS_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -b DEBUG \
    -a X64 -n %{?_smp_flags}

OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=FALSE \
    -D NETWORK_IP6_ENABLE=FALSE \
    -D IPXE_ENABLE=TRUE \
    -D HTTP_BOOT_ENABLE=FALSE \
    -D TLS_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -b RELEASE \
    -a X64 -n %{?_smp_flags}


%install
install -m 755 -d %{buildroot}/%{_datadir}/%{name}
install -m 644 Build/OvmfX64/DEBUG_GCC*/FV/OVMF.fd %{buildroot}/%{_datadir}/%{name}/OVMF-debug.fd
install -m 644 Build/OvmfX64/RELEASE_GCC*/FV/OVMF.fd %{buildroot}/%{_datadir}/%{name}/OVMF-release.fd
ln -sf OVMF-release.fd %{buildroot}/%{_datadir}/%{name}/OVMF.fd

cp OvmfPkg/License.txt License.ovmf
# cp CryptoPkg/Library/OpensslLib/openssl-xs/LICENSE LICENSE.openssl


%files
%license License.txt
%license License.ovmf
#%license LICENSE.openssl
%{_datadir}/%{name}


%changelog
* Tue Dec 18 2018 Edwin Török <edvin.torok@citrix.com> - 20180522git4b8552d-1.2.0
- CA-293636: Add support for NVIDIA vGPU on top of UEFI
- CA-293633: Set default video resoultion to 1024x768
- CA-293634: Various fixes to make GPU/PCI passthrough work
- Add a config option to use iPXE drivers
- Cleanup XenVariable integration
- CA-297602: Speedup boot by enabling PV drivers
- CA-298449: Add basic support for Intel GVT-g on top of UEFI
- Fix race finding XenVariable PCI device
- CA-296489: Allow boot ordering to be set from XS
- CA-296489: Make Xen boot ordering work with normal boot entries
- Remove unused patches
- CA-296489: XenBootOrder: Fix a typo
- CP-28675: XenVariable: Make some functions static
- CP-28675: XenVariable: Move useful functions into a header file
- CP-28675: XenVariable: Notify dom0 on Security Violation
- CP-29100: Remove PCI Device and expose IO port for communication with varstored.
- CP-29100: Remove previous workaround related to Xen Variable PCI device
- CA-297688: Keep caching enabled during SEC phase

* Thu May 17 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 20170920git947f373-1.0.0
- Initial packaging.
