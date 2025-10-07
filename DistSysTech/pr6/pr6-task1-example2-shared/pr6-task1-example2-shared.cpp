#include <stdio.h>
#include <omp.h>

int main() {
	int n = 6; // Кількість ітерацій
	int i, a[6] = { 0 }; // Лічильник ітерацій та масив для збереження результатів
#pragma omp parallel for shared(a)
	for (i = 0; i < n; i++)
	{
		a[i] += i;
		printf("Thread %d has a value of a[%d] = %d for i = %d\n",
			omp_get_thread_num(), i, a[i], i);
	}
}