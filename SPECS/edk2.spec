%global package_speccommit 3cab3ff7d054278e785cadb0c91847a444063912
%global usver 20180522git4b8552d
%global xsver 1.5.0
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 4b8552d

Name: edk2
Summary: EFI Development Kit II
Version: 20180522git4b8552d
Release: %{?xsrel}%{?dist}

License: BSD and MIT
URL: https://github.com/tianocore/edk2
Source0: edk2-20180522git4b8552d.tar.gz
Patch0: 0001-OvmfPkg-XenSupport-remove-usage-of-prefetchable-PCI-.patch
Patch1: 0002-OvmfPkg-XenSupport-use-a-correct-PCI-host-bridge-ape.patch
Patch2: 0003-OvmfPkg-XenSupport-turn-off-address-decoding-before-.patch
Patch3: 0001-OvmfPkg-End-timer-interrupt-later-to-avoid-stack-ove.patch
Patch4: 0001-fix-type-in-ini-py.patch
Patch5: 0001-MdePkg-TimerRngLib-Added-RngLib-that-uses-TimerLib.patch
Patch6: 0001-OvmfPkg-Add-RngLib-based-on-TimerLib-for-Crypto.patch
Patch7: 0001-SecurityPkg-TPM-Import-PeiDxeTpmPlatformHierarchyLib.patch
Patch8: 0002-SecurityPkg-TPM-Fix-bugs-in-imported-PeiDxeTpmPlatfo.patch
Patch9: 0003-SecrutiyPkg-Tcg-Import-Tcg2PlatformDxe-from-edk2-pla.patch
Patch10: 0004-SecurityPkg-Tcg-Make-Tcg2PlatformDxe-buildable-and-f.patch
Patch11: 0005-SecurityPkg-Introduce-new-PCD-PcdRandomizePlatformHi.patch
Patch12: 0006-SecurityPkg-Tcg-Import-Tcg2PlatformPei-from-edk2-pla.patch
Patch13: 0007-SecurityPkg-Tcg-Make-Tcg2PlatformPei-buildable-and-f.patch
Patch14: 0008-SecurityPkg-Add-references-to-header-and-inf-files-t.patch
Patch15: 0001-OvmfPkg-Reference-new-Tcg2PlatformPei-in-the-build-s.patch
Patch16: 0002-OvmfPkg-Reference-new-Tcg2PlatformDxe-in-the-build-s.patch
Patch17: 0003-OvmfPkg-Handle-TPM-2-physical-presence-opcodes-much-.patch
Patch18: 0004-OvmfPkg-TPM-PPI-Connect-default-consoles-for-user-in.patch
Patch19: 0001-OvmfPkg-Call-PlatformInitializeConsole-for-GPU-passt.patch
Patch20: ovmfpkg__add_tcg2_configuration_menu_to_the_device_manager_menu.patch
Patch21: 0001-OvmfPkg-XenPlatformPei-Use-CPUID-to-get-physical-add.patch
Patch22: ovmfpkg-xenpvblkdxe__fix_memory_barrier_macro.patch
Patch23: openssl.patch
Patch24: nvidia-vgpu-support.patch
Patch25: gvt-g-support.patch
Patch26: set-default-resolution-1024-768.patch
Patch27: embed-nic-drivers.patch
Patch28: add-xen-variable.patch
Patch29: add-xen-platform-device-id.patch
Patch30: disable-modules.patch
Patch31: xenorder.patch
Patch32: keep-caching-enabled.patch
Patch33: remove-unused-crypto.patch
Patch34: add-Tcg2PhysicalPresenceLibXen.patch
Patch35: tcg2config-fix-operation-parameter-prompt.patch
Patch36: set-tpm2-acpi-table-revision.patch
Patch37: disable-config-option-in-TCG2-config-screen.patch

BuildRequires: gcc gcc-c++
BuildRequires: python
BuildRequires: libuuid-devel
BuildRequires: nasm
BuildRequires: iasl
BuildRequires: ipxe-efi
%{?_cov_buildrequires}


%description
Provides the Open Virtual Machine Firmware (OVMF) built for x64.
This is a build of the EFI Development Kit II suitable for using
as firmware in a virtual machine.


%prep
%autosetup -p1
%{?_cov_prepare}


%build
cp %{_datadir}/ipxe/10ec8139.efi .
cp %{_datadir}/ipxe/8086100e.efi .

%{?_cov_wrap} OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=TRUE \
    -D NETWORK_IP6_ENABLE=FALSE \
    -D IPXE_ENABLE=TRUE \
    -D HTTP_BOOT_ENABLE=FALSE \
    -D TLS_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -D TPM2_ENABLE \
    -D TPM2_CONFIG_ENABLE \
    -b DEBUG \
    -a X64 -n %{?_smp_flags}

%{?_cov_wrap} OvmfPkg/build.sh \
    -D SECURE_BOOT_ENABLE=TRUE \
    -D NETWORK_IP6_ENABLE=FALSE \
    -D IPXE_ENABLE=TRUE \
    -D HTTP_BOOT_ENABLE=FALSE \
    -D TLS_ENABLE=FALSE \
    -D XEN_VARIABLE_ENABLE=TRUE \
    -D EXTRA_MODULES_ENABLE=FALSE \
    -D FD_SIZE_2MB \
    -D TPM2_ENABLE \
    -D TPM2_CONFIG_ENABLE \
    -b RELEASE \
    -a X64 -n %{?_smp_flags}


%install
install -m 755 -d %{buildroot}/%{_datadir}/%{name}
install -m 644 Build/OvmfX64/DEBUG_GCC*/FV/OVMF.fd %{buildroot}/%{_datadir}/%{name}/OVMF-debug.fd
install -m 644 Build/OvmfX64/RELEASE_GCC*/FV/OVMF.fd %{buildroot}/%{_datadir}/%{name}/OVMF-release.fd
ln -sf OVMF-release.fd %{buildroot}/%{_datadir}/%{name}/OVMF.fd

cp OvmfPkg/License.txt License.ovmf
# cp CryptoPkg/Library/OpensslLib/openssl-xs/LICENSE LICENSE.openssl

%{?_cov_install}


%files
%license License.txt
%license License.ovmf
#%license LICENSE.openssl
%{_datadir}/%{name}

%{?_cov_results_package}


%changelog
* Wed Aug 17 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.5.0
- Add TPM support

* Mon Aug 01 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.8
- CA-343027: Fix hang in OVMF

* Fri Jun 17 2022 Mark Syms <mark.syms@citrix.com> - 20180522git4b8552d-1.4.7
- Fix script typo which breaks static analysis

* Mon Feb 21 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.6
- CP-38416: Enable static analysis

* Mon Jan 18 2021 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.5
- CA-350259: Fix PCI passthrough of devices with 64+ GB BARs

* Fri Dec 04 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.4
- CP-35517: Bump release to rebuild

* Wed Jun 24 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.3
- CA-337679: Fix triple fault while booting on a heavy loaded host

* Thu Jul 04 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.2
- CA-322248: Prevent guest attempting to accessing priv regsiters

* Wed Jun 19 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 20180522git4b8552d-1.4.1
- CA-321788: make vGPU console work with all NVidia cards
- Replace local fixes with upstream backports

* Thu May 30 2019 Edwin Török <edvin.torok@citrix.com> - 20180522git4b8552d-1.4.0
- CP-30786: Turn off cryptopkg when secure boot is off
- Fix typo in secure boot enable condition
- CA-314662: Don't accidentally switch off MTRRs in SEC phase
- CA-309841: reenable PV drivers in OVMF
- CP-30787: disable unneeded crypto code, simplify patchqueue

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
