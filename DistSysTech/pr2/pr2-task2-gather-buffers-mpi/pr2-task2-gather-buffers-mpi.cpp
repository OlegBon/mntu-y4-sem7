#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 10 // ����� ���������� ������

int main(int argc, char** argv) {
    int rank, size;
    int buffer[SIZE];
    double start_time, end_time;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // ����������� ���������� ������
    for (int i = 0; i < SIZE; ++i)
        buffer[i] = rank * 10 + i;

    // ���� ���������� ������ �� ������� �����
    printf("Initial buffer on rank %d: ", rank);
    for (int i = 0; i < SIZE; ++i)
        printf("%d ", buffer[i]);
    printf("\n");

    // ���������� ���� ��������
    start_time = MPI_Wtime();

    if (rank != 0) {
        // ����� 1...n ���������� ��� ������ �� rank 0
        MPI_Send(buffer, SIZE, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }
    else {
        // rank 0 ������ ������ �� ����� �����
        int* full_buffer = (int*)malloc(SIZE * size * sizeof(int));

        // ������� ������� �����
        for (int i = 0; i < SIZE; ++i)
            full_buffer[i] = buffer[i];

        // ������ ������ �� ����� �����
        for (int i = 1; i < size; ++i) {
            MPI_Recv(&full_buffer[i * SIZE], SIZE, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
        }

        // ���������� ����
        end_time = MPI_Wtime();

        // ���� ���������� �������� ������ �� ���� �����
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