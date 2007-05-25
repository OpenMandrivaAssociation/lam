%define name    lam
%define version 7.1.2
%define release %mkrel 3
%define major           7
%define libname %mklibname %name %{major}

Name: 		    %{name}
Version: 	    %{version}
Release: 	    %{release}
Summary:        The LAM (Local Area Multicomputer) programming environment.
License: 	    BSD
Group: 		    Development/Other
URL: 		    http://www.lam-mpi.org/
Source: 	    %{name}-%{version}.tar.bz2
Source3:	    rhosts
Source4:	    test_mpi.c
Obsoletes:      %{name}-runtime
BuildRequires: 	gcc-gfortran
BuildRoot: 	    %{_tmppath}/%{name}-%{version}

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

%package 	devel
Summary: 	Development binaries for lam environment
Group: 		Development/Other
Requires:	%{libname}-devel = %{version}
Conflicts:  mpic++
Conflicts:  mpicc
Conflicts:  mpif77
Conflicts:  mpich2
Conflicts:  mpi2cc
Conflicts:  mpi2f77

%description devel
LAM development binaries for compiling parallel programs.

%package 	doc
Summary: 	Documentation for developing programs that will use lam-mpi
Group: 		Development/Other

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

%package 	-n %{libname}-devel
Summary: 	Headers for developing programs that will use lam-mpi
Group: 		Development/Other
Conflicts:  mpich2-devel
Conflicts:  mpich1-devel

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

%build
%configure --sysconfdir=%{_sysconfdir}/lam \
	--with-rpi=sysv \
	--with-rsh=%{_bindir}/rsh \
	--with-trillium \
	--with-romio \
	--with-fc=%{_bindir}/gfortran
%make all

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

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
%{_mandir}/man1/hboot.1.bz2
%{_mandir}/man1/lamboot.1.bz2
%{_mandir}/man1/lamhalt.1.bz2
%{_mandir}/man1/lamnodes.1.bz2
%{_mandir}/man1/lamclean.1.bz2
%{_mandir}/man1/lamexec.1.bz2
%{_mandir}/man1/lamgrow.1.bz2
%{_mandir}/man1/lamshrink.1.bz2
%{_mandir}/man1/lamtrace.1.bz2
%{_mandir}/man1/wipe.1.bz2
%{_mandir}/man1/mpimsg.1.bz2
%{_mandir}/man1/mpirun-lam.1.bz2
%{_mandir}/man1/mpitask.1.bz2
%{_mandir}/man1/recon.1.bz2
%{_mandir}/man1/tkill.1.bz2
%{_mandir}/man1/tping.1.bz2
%{_mandir}/man1/laminfo.1.bz2
%{_mandir}/man1/mpiexec-lam.1.bz2
%{_mandir}/man7/lamssi.7.bz2
%{_mandir}/man7/lamssi_boot.7.bz2
%{_mandir}/man7/lamssi_coll.7.bz2
%{_mandir}/man7/lamssi_cr.7.bz2
%{_mandir}/man7/lamssi_rpi.7.bz2
%{_mandir}/man1/lamcheckpoint.1.bz2
%{_mandir}/man1/lamrestart.1.bz2
%{_mandir}/man1/lamwipe.1.bz2
%{_mandir}/man3/MPI_Alltoallw.3.bz2
%{_mandir}/man3/MPI_Exscan.3.bz2
%{_mandir}/man7/libmpi.7.bz2
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
%{_mandir}/man1/bfctl.1.bz2
%{_mandir}/man1/bfstate.1.bz2
%{_mandir}/man1/doom.1.bz2
%{_mandir}/man1/fctl.1.bz2
%{_mandir}/man1/fstate.1.bz2
%{_mandir}/man1/loadgo.1.bz2
%{_mandir}/man1/state.1.bz2
%{_mandir}/man1/sweep.1.bz2
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
%{_mandir}/man1/hcc.1.bz2
%{_mandir}/man1/hcp.1.bz2
%{_mandir}/man1/hf77.1.bz2
%{_mandir}/man1/introu.1.bz2
%{_mandir}/man1/mpiCC.1.bz2
%{_mandir}/man1/mpicc.1.bz2
%{_mandir}/man1/mpif77.1.bz2
%{_mandir}/man1/lamd.1.bz2
%{_mandir}/man1/mpic++.1.bz2
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
