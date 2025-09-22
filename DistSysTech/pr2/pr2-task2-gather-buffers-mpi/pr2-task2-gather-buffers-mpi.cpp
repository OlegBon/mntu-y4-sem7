#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 10 // Розмір локального буфера

int main(int argc, char** argv) {
    int rank, size;
    int buffer[SIZE];
    double start_time, end_time;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Ініціалізація локального буфера
    for (int i = 0; i < SIZE; ++i)
        buffer[i] = rank * 10 + i;

    // Вивід локального буфера на кожному ранку
    printf("Initial buffer on rank %d: ", rank);
    for (int i = 0; i < SIZE; ++i)
        printf("%d ", buffer[i]);
    printf("\n");

    // Вимірювання часу передачі
    start_time = MPI_Wtime();

    if (rank != 0) {
        // Вузли 1...n надсилають свої буфери до rank 0
        MPI_Send(buffer, SIZE, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }
    else {
        // rank 0 приймає буфери від інших вузлів
        int* full_buffer = (int*)malloc(SIZE * size * sizeof(int));

        // Копіюємо власний буфер
        for (int i = 0; i < SIZE; ++i)
            full_buffer[i] = buffer[i];

        // Прийом буферів від інших ранків
        for (int i = 1; i < size; ++i) {
            MPI_Recv(&full_buffer[i * SIZE], SIZE, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
        }

        // Вимірювання часу
        end_time = MPI_Wtime();

        // Вивід фінального зібраного буфера як один масив
        printf("\nFinal gathered buffer on rank 0:\n");
        for (int i = 0; i < SIZE * size; ++i)
            printf("%d ", full_buffer[i]);
        printf("\n");

        printf("Total receive time: %.6f seconds\n", end_time - start_time);
        free(full_buffer);
    }

    MPI_Finalize();
    return 0;
}