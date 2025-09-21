#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    int myrank, size;

    MPI_Init(&argc, &argv); // ����������� MPI
	MPI_Comm_size(MPI_COMM_WORLD, &size); // ��������� ������ �����������
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	// �������� ����� �������
    printf("Proc %d of %d\n", myrank, size);

	MPI_Finalize(); // Գ�������� MPI puts("Done");

    return 0;
    getchar();
}