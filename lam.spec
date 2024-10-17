%define name    lam
%define version 7.1.4
%define release 3
%define major           7
%define libname %mklibname %name %{major}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The LAM (Local Area Multicomputer) programming environment
License:	BSD
Group:		System/Cluster
URL:		https://www.lam-mpi.org/
Source0:		%{name}-%{version}.tar.bz2
Source3:	rhosts
Source4:	test_mpi.c
Patch0:		lamdebug_formatliteral.patch
Patch1:		show_help_formatliteral.patch
Patch2:		fprintfusage_formatliteral.patch
Patch3:		lamgrow_formatliteral.patch
Patch4:		mpitask_formatliteral.patch
Obsoletes:	%{name}-runtime
BuildRequires:	gcc-gfortran
BuildRequires:	gcc-c++, gcc, gcc-cpp

%description 
LAM (Local Area Multicomputer) is an Message-Passing Interface (MPI)
programming environment and development system for heterogeneous
computers on a network. With LAM/MPI, a dedicated cluster or an
existing network computing infrastructure can act as one parallel
computer to solve one problem. LAM/MPI is considered to be "cluster
friendly" because it offers daemon-based process startup/control as
well as fast client-to-client message passing protocols. LAM/MPI can
use TCP/IP and/or shared memory for message passing (different RPMs
are supplied for this -- see the main LAM website at
http://www.mpi.nd.edu/lam/ for details).

LAM features a full implementation of MPI version 1 (with the
exception that LAM does not support cancelling of sends), and much of
version 2. Compliant applications are source code portable between LAM
and any other implementation of MPI. In addition to meeting the
standard, LAM/MPI offers extensive monitoring capabilities to support
debugging. Monitoring happens on two levels: On one level, LAM/MPI has
the hooks to allow a snapshot of a process and message status to be
taken at any time during an application run. The status includes all
aspects of synchronization plus datatype map/signature, communicator
group membership and message contents (see the XMPI application on the
main LAM website). On the second level, the MPI library can produce a
cumulative record of communication, which can be visualized either at
runtime or post-mortem.

%package devel
Summary: 	Development binaries for lam environment
Group:		System/Cluster
Requires:	%{libname}-devel = %{version}
Conflicts:	mpic++
Conflicts:	mpicc
Conflicts:	mpif77
Conflicts:	mpich2
Conflicts:	mpi2cc
Conflicts:	mpi2f77

%description devel
LAM development binaries for compiling parallel programs.

%package doc
Summary: 	Documentation for developing programs that will use lam-mpi
Group: 		System/Cluster

%description doc
LAM (Local Area Multicomputer) is an Message-Passing Interface (MPI)
programming environment and development system for heterogeneous
computers on a network. With LAM/MPI, a dedicated cluster or an
existing network computing infrastructure can act as one parallel
computer to solve one problem. LAM/MPI is considered to be "cluster
friendly" because it offers daemon-based process startup/control as
well as fast client-to-client message passing protocols. LAM/MPI can
use TCP/IP and/or shared memory for message passing (different RPMs
are supplied for this -- see the main LAM website at
http://www.mpi.nd.edu/lam/ for details).

LAM features a full implementation of MPI version 1 (with the
exception that LAM does not support cancelling of sends), and much of
version 2. Compliant applications are source code portable between LAM
and any other implementation of MPI. In addition to meeting the
standard, LAM/MPI offers extensive monitoring capabilities to support
debugging. Monitoring happens on two levels: On one level, LAM/MPI has
the hooks to allow a snapshot of a process and message status to be
taken at any time during an application run. The status includes all
aspects of synchronization plus datatype map/signature, communicator
group membership and message contents (see the XMPI application on the
main LAM website). On the second level, the MPI library can produce a
cumulative record of communication, which can be visualized either at
runtime or post-mortem.

This package provides the documentation needed to develop
applications using the lam libraries.

%package -n %{libname}-devel
Summary: 	Headers for developing programs that will use lam-mpi
Group:		System/Cluster
Conflicts:	mpich2-devel
Conflicts:	mpich1-devel

%description -n %{libname}-devel
LAM (Local Area Multicomputer) is an Message-Passing Interface (MPI)
programming environment and development system for heterogeneous
computers on a network. With LAM/MPI, a dedicated cluster or an
existing network computing infrastructure can act as one parallel
computer to solve one problem. LAM/MPI is considered to be "cluster
friendly" because it offers daemon-based process startup/control as
well as fast client-to-client message passing protocols. LAM/MPI can
use TCP/IP and/or shared memory for message passing (different RPMs
are supplied for this -- see the main LAM website at
http://www.mpi.nd.edu/lam/ for details).

LAM features a full implementation of MPI version 1 (with the
exception that LAM does not support cancelling of sends), and much of
version 2. Compliant applications are source code portable between LAM
and any other implementation of MPI. In addition to meeting the
standard, LAM/MPI offers extensive monitoring capabilities to support
debugging. Monitoring happens on two levels: On one level, LAM/MPI has
the hooks to allow a snapshot of a process and message status to be
taken at any time during an application run. The status includes all
aspects of synchronization plus datatype map/signature, communicator
group membership and message contents (see the XMPI application on the
main LAM website). On the second level, the MPI library can produce a
cumulative record of communication, which can be visualized either at
runtime or post-mortem.

This package provides the static libraries and header files needed to compile
applications using the lam libraries.

%prep
%setup -q -n %{name}-%{version}
%patch0
%patch1
%patch2
%patch3
%patch4

%build
# clang don't support the bool data type
export CC=gcc
export CXX=g++

%configure2_5x --sysconfdir=%{_sysconfdir}/lam \
	--with-rpi=sysv \
	--with-rsh=%{_bindir}/rsh \
	--with-trillium \
	--with-romio \
	--with-fc=%{_bindir}/gfortran
%make all

%install
%makeinstall_std

mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
cat > %{buildroot}/%{_sysconfdir}/profile.d/%{name}.csh <<EOF
setenv LAMHELPFILE /etc/lam/lam-helpfile
EOF
cat > %{buildroot}/%{_sysconfdir}/profile.d/%{name}.sh <<EOF
export LAMHELPFILE=/etc/lam/lam-helpfile
EOF

# A sample mpi program (hello world)
%{buildroot}%{_bindir}/hcc \
    -I%{buildroot}%{_includedir} \
    -L%{buildroot}%{_libdir} \
    -o %{buildroot}/%{_bindir}/test_mpi.%{name} \
    %{SOURCE4}

# Fix conflict with mpich package
mv %{buildroot}%{_mandir}/man1/mpirun.1 %{buildroot}%{_mandir}/man1/mpirun-lam.1
mv %{buildroot}%{_mandir}/man1/mpiexec.1 %{buildroot}%{_mandir}/man1/mpiexec-lam.1
mv %{buildroot}%{_bindir}/mpirun %{buildroot}%{_bindir}/mpirun-lam
mv %{buildroot}%{_bindir}/mpiexec %{buildroot}%{_bindir}/mpiexec-lam

# move documentation at the correct place
install -d -m 755 %{buildroot}%{_datadir}/doc
mv %{buildroot}%{_datadir}/lam/doc %{buildroot}%{_datadir}/doc/%{name}-doc-%{version}
rm -rf %{buildroot}%{_datadir}/lam

cat > README.urpmi <<EOF
Post-installation procedure:
- create a user with constant uid/gid and shared home directory on all nodes
- ensure this user has rsh/ssh access to all nodes
EOF

%files
%defattr(-,root,root)
%doc LICENSE README.urpmi
%{_bindir}/lamclean
%{_bindir}/lamexec
%{_bindir}/lamgrow
%{_bindir}/lamshrink
%{_bindir}/lamtrace
%{_bindir}/mpimsg
%{_bindir}/mpirun-lam
%{_bindir}/mpiexec-lam
%{_bindir}/mpitask
%{_bindir}/lamd
%{_bindir}/tping
%{_bindir}/hboot
%{_bindir}/lamboot
%{_bindir}/lamhalt
%{_bindir}/lamnodes
%{_bindir}/recon
%{_bindir}/tkill
%{_bindir}/wipe
%{_bindir}/lamd_bforward
%{_bindir}/lamd_bufferd
%{_bindir}/lamd_dli_inet
%{_bindir}/lamd_dlo_inet
%{_bindir}/lamd_echod
%{_bindir}/lamd_filed
%{_bindir}/lamd_flatd
%{_bindir}/lamd_haltd
%{_bindir}/lamd_iod
%{_bindir}/lamd_kenyad
%{_bindir}/lamd_kernel
%{_bindir}/lamd_loadd
%{_bindir}/lamd_router
%{_bindir}/lamd_traced
%{_bindir}/lamd_versiond
%{_bindir}/laminfo
%{_bindir}/mpic++
%{_bindir}/lamcheckpoint
%{_bindir}/lamrestart
%{_bindir}/lamwipe
%{_bindir}/test_mpi.%{name}
%{_mandir}/man1/hboot.*
%{_mandir}/man1/lamboot.*
%{_mandir}/man1/lamhalt.*
%{_mandir}/man1/lamnodes.*
%{_mandir}/man1/lamclean.*
%{_mandir}/man1/lamexec.*
%{_mandir}/man1/lamgrow.*
%{_mandir}/man1/lamshrink.*
%{_mandir}/man1/lamtrace.*
%{_mandir}/man1/wipe.*
%{_mandir}/man1/mpimsg.*
%{_mandir}/man1/mpirun-lam.*
%{_mandir}/man1/mpitask.*
%{_mandir}/man1/recon.*
%{_mandir}/man1/tkill.*
%{_mandir}/man1/tping.*
%{_mandir}/man1/laminfo.*
%{_mandir}/man1/mpiexec-lam.*
%{_mandir}/man1/lamcheckpoint.*
%{_mandir}/man1/lamrestart.*
%{_mandir}/man1/lamwipe.*
# For Trillium Option
%{_bindir}/bfctl
%{_bindir}/bfstate
%{_bindir}/doom
%{_bindir}/fctl
%{_bindir}/fstate
%{_bindir}/loadgo
%{_bindir}/state
%{_bindir}/sweep
%{_bindir}/kdump
%{_bindir}/ipcdr
%{_bindir}/filedr
%{_mandir}/man1/bfctl.*
%{_mandir}/man1/bfstate.*
%{_mandir}/man1/doom.*
%{_mandir}/man1/fctl.*
%{_mandir}/man1/fstate.*
%{_mandir}/man1/loadgo.*
%{_mandir}/man1/state.*
%{_mandir}/man1/sweep.*
#End of Trillium Option
%config(noreplace) %{_sysconfdir}/lam
%config(noreplace) %{_sysconfdir}/profile.d/*

%files devel
%defattr(-,root,root)
%doc LICENSE
%{_bindir}/hcc
%{_bindir}/hf77
%{_bindir}/hcp
%{_bindir}/mpicc
%{_bindir}/mpiCC
%{_bindir}/mpif77
%{_mandir}/man1/hcc.*
%{_mandir}/man1/hcp.*
%{_mandir}/man1/hf77.*
%{_mandir}/man1/introu.*
%{_mandir}/man1/mpiCC.*
%{_mandir}/man1/mpicc.*
%{_mandir}/man1/mpif77.*
%{_mandir}/man1/lamd.*
%{_mandir}/man1/mpic++.*
%{_mandir}/mans/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files -n %{name}-doc
%defattr(-,root,root)
%{_datadir}/doc/%{name}-doc-%{version}
      
%files -n %{libname}-devel
%defattr(-,root,root)
%doc LICENSE
%{_libdir}/lam
%{_libdir}/lib*
%{_includedir}/*
%{_mandir}/man2/*
%{_mandir}/man3/*


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 7.1.4-2mdv2011.0
+ Revision: 612694
- the mass rebuild of 2010.1 packages

* Thu Sep 10 2009 Stéphane Téletchéa <steletch@mandriva.org> 7.1.4-1mdv2010.0
+ Revision: 436576
- Updated format fixes
- Back to 0.7.4-1 since no other build passed the bs
- More format string fixes
- Update to latest stable release
- Use new configure macro
- Correct format string for some files

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 7.1.3-2mdv2008.1
+ Revision: 136535
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix man pages

* Fri Jun 22 2007 Nicolas Vigier <nvigier@mandriva.com> 7.1.3-2mdv2008.0
+ Revision: 43001
- remove dot from summary (for rpmlint warning)
- use tabs instead of a mix of spaces and tabs
- Change group to System/Cluster

* Fri May 25 2007 Nicolas Vigier <nvigier@mandriva.com> 7.1.3-1mdv2008.0
+ Revision: 31099
- update to version 7.1.3
- Import lam



* Thu Aug 31 2006 Guillaume Rousse <guillomovitch@mandriva.org> 7.1.2-3mdv2007.0
- better consistency with mpich package:
 - rename lam-runtime subpackage to lam
 - no more user creation in %%post, as it was too simplist to work, but advertise
   post-installation procedure through README.urpmi
- fix conflicts by renaming binaries in runtime package, with explicit conflicts in devel package
- move doc files in standard location
- move man pages from doc to lib devel package
- drop %%preun script, another solution is still needed
- spec cleanups

* Thu Jun 22 2006 Erwan Velu <erwan@seanodes.com> 7.1.2-2
- FixingP provides

* Wed Jun 13 2006 Erwan Velu <erwan@seanodes.com> 7.1.2-1mdk
- 7.1.2
- Removing gfortan hardcoded version
- There is no need to Buildrequires libmpich2_1-devel

* Fri Oct 28 2005 Antoine Ginies <aginies@n1.mandriva.com> 7.1.1-3mdk
- fix attr pb

* Fri Oct 28 2005 Antoine Ginies <aginies@n1.mandriva.com> 7.1.1-2mdk
- remove unwanted link to mpic++.h
- add missing Buildrequire: libmpich2_1-devel

* Wed Aug 24 2005 Erwan Velu <erwan@seanodes.com> 7.1.1-1mdk
- 7.1.1
- Using gfortan instead of gcc-f77
* Fri Jun 25 2004 Erwan Velu <erwan@mandrakesoft.com> 7.0.6-2mdk
- Rebuild
* Fri Jun 11 2004 Erwan Velu <erwan@mandrakesoft.com> 7.0.6-1mdk
- 7.0.6
* Fri Feb 26 2004 Erwan Velu <erwan@mandrakesoft.com> 7.0.4-2mdk
- Rebuild
* Thu Feb 19 2004 Erwan Velu <erwan@mandrakesoft.com> 7.0.4-1mdk
- New release (waow since a really long time)
* Wed May 28 2003 Erwan Velu <erwan@mandrakesoft.com> 6.5.9-4mdk
- Removing mklibname
* Wed May 28 2003 Erwan Velu <erwan@mandrakesoft.com> 6.5.9-3mdk
- ifarching x86_64
* Wed  Jan 29 2003 Erwan Velu <erwan@mandrakesoft.com> 6.5.9-2mdk
- Final release
* Mon Jan 20 2003 Erwan Velu <erwan@mandrakesoft.com> 6.5.9-1mdk
- New version
* Thu Jan 16 2003 Erwan Velu <erwan@mandrakesoft.com> 6.5.8-4mdk
- Rebuild for new glibc
- Fixing missing errno.h
* Wed Nov 20 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 6.5.8-3mdk
- Fixing missing files
* Wed Nov 20 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 6.5.8-2mdk
- Relocating lam binaries 
- Changing mpirun to mpirun-lam for removing conflicts with mpich
* Wed Nov 20 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 6.5.8-1mdk
- New version
- Fixing path for removing conflicts with mpich
- Changing mpirun.1 in mpirun-lam.1 to avoid mpich conflict
* Mon Sep 02 2002 Lenny Cartier <lenny@mandrakesodft.com> 6.5.6-16mdk
- rebuild
* Tue Aug 6 2002 Antoine Ginies <aginies@mandrakesoft.com> 6.5.6-15mdk
- build with gcc 3.2
* Mon Jun 17 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-14mdk
- Fixing missing requires
- Adding noreplace on config files
* Thu Jun 06 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-13mdk
- Fixing mpi user id
- Fixing wrong perm on sample script
* Wed Jun 05 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-12mdk
- Fixing .bashrc for mpi
* Tue Jun 04 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-11mdk
- Fixing conflict between libmpich0-devel and lam-doc
* Tue Jun 04 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-10mdk
- Fixing wrong right on sample script
- Changing sample script
* Fri May 31 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-9mdk
- Removing virtual MPI provides
- Adding hello world mpi sample program
* Tue May 28 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-8mdk
- Adding conflicts on all packages

* Tue May 28 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-7mdk
- Stopping lam before uninstalling package

* Mon May 27 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-6mdk
- Fixing late friday changes :-)
- Proving virtual Mpi is now fixed

* Fri May 24 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-5mdk
- Adding mpi user
- Providing virtual Mpi
- Adding sample rhost configuration file

* Fri May 24 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-4mdk
- Added Trillium option (devel option), man pages and binaries
- Creating devel package
- Cleaning liblam0-devel package

* Fri May 24 2002 Erwan Velu <erwan@mandrakesoft.com> 6.5.6-3mdk
- Gcc 3.1 build
- Cleaning Spec file

* Tue Nov 27 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 6.5.6-2mdk
- Added Conflict tag for mpich conflicts

* Tue Nov 27 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 6.5.6-1mdk
- 6.5.6

* Fri Nov 23 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 6.5.5-3mdk
- Added include files missed from last upload

* Thu Nov 22 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 6.5.5-2mdk
- rebuild

* Mon Nov 19 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 6.5.5-1mdk
- First version of the package
