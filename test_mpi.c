/*
 * Author:  Matt Massie (massie@cs.berkeley.edu)
 * 
 * Originally Copied from:
 * http://now.CS.Berkeley.EDU/Fastcomm/MPI/howto/hello-world/hello-world.c
 * by Frederick Wong (fredwong@cs.berkeley.edu)
 */
#include <stdio.h>
#include "mpi.h"
#include <unistd.h>

int
main(int argc, char **argv) {

  int rank;
  char msg[20];
  char host[255];
  
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  gethostname(host,254);
  
  if (rank==0) {
    strcpy(msg,"Hello World!");
    printf("%s: Sending %s\n\n",host,msg);
    MPI_Bcast(msg, 13, MPI_CHAR, rank, MPI_COMM_WORLD);
  } else {
    MPI_Bcast(msg, 13, MPI_CHAR, 0, MPI_COMM_WORLD);
    printf("  |- %-30s %s\n", host,msg);
  }

  MPI_Finalize();
}
