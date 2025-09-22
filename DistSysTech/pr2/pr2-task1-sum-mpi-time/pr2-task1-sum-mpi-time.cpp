#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    const int N = 10000000; // Загальна кількість чисел для сумування

    int myrank, totalnodes;
    //int sum = 0, startval, endval, accum;
    long long sum = 0, startval, endval, accum;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    // Початок вимірювання часу
    double start_time = MPI_Wtime();

    // Розрахунок діапазону
    startval = N * myrank / totalnodes + 1;
    endval = N * (myrank + 1) / totalnodes;

    for (int i = startval; i <= endval; ++i)
        sum += i;

    if (myrank != 0) {
        //MPI_Send(&sum, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
        MPI_Send(&sum, 1, MPI_LONG_LONG, 0, 1, MPI_COMM_WORLD);
    }
    else {
        for (int j = 1; j < totalnodes; ++j) {
            //MPI_Recv(&accum, 1, MPI_INT, j, 1, MPI_COMM_WORLD, &status);
            MPI_Recv(&accum, 1, MPI_LONG_LONG, j, 1, MPI_COMM_WORLD, &status);
            sum += accum;
        }

        // Кінець вимірювання часу
        double end_time = MPI_Wtime();
        double elapsed = end_time - start_time;

        printf("Output: (on %d nodes)\n", totalnodes);
        //printf("Sum from 1 to %d: %d\n", N, sum);
        printf("Sum from 1 to %d: %lld\n", N, sum);
        printf("Execution time: %.6f seconds\n", elapsed);
    }

    MPI_Finalize();
    return 0;
}