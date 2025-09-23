#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    int rank, size;
    int x, y;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Кожен процес має своє значення x
    x = rank + 1; // x0 = 1, x1 = 2, ...

    // Префіксна сума
    MPI_Scan(&x, &y, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

    // Вивід результату
    printf("Rank %d: x = %d -> Prefix sum y = %d\n", rank, x, y);

    MPI_Finalize();
    return 0;
}