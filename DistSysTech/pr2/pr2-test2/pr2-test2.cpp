#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    int myrank, size;

    MPI_Init(&argc, &argv); // Ініціалізація MPI
	MPI_Comm_size(MPI_COMM_WORLD, &size); // Отримання розміру комунікатора
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	// Отримуємо номер процесу
    printf("Proc %d of %d\n", myrank, size);

	MPI_Finalize(); // Фіналізація MPI puts("Done");

    return 0;
    getchar();
}