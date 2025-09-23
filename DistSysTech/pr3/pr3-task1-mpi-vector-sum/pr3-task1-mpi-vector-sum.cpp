#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define N 24 // довжина вектора

int main(int argc, char** argv) {
    int rank, size;
    float data[N], local_sum = 0.0, total_sum = 0.0;


    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int chunk = N / size;

    float* recvbuf = (float*)malloc(chunk * sizeof(float));
    // Перевірка виділення пам'яті
    if (recvbuf == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    // Ініціалізація вектора на root
    if (rank == 0) {
        for (int i = 0; i < N; ++i)
            data[i] = static_cast<float>(i + 1);
    }

    // Розподіл підвекторів
    MPI_Scatter(data, chunk, MPI_FLOAT, recvbuf, chunk, MPI_FLOAT, 0, MPI_COMM_WORLD);

    // Часткова сума
    local_sum = 0.0;
    for (int i = 0; i < chunk; ++i)
        local_sum += recvbuf[i];

    printf("Rank %d received: ", rank);
    for (int i = 0; i < chunk; ++i)
        printf("%.1f ", recvbuf[i]);
    printf("-> Local sum = %.1f\n", local_sum);

    // Збір часткових сум
    MPI_Reduce(&local_sum, &total_sum, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Вивід результату
    if (rank == 0) {
        printf("Total sum = %.2f\n", total_sum);
    }

    free(recvbuf);
    MPI_Finalize();
    return 0;
}