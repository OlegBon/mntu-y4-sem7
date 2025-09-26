#include <omp.h>
#include <stdio.h>

int main()
{
	//omp_set_num_threads(6); // Задаємо кількість потоків у паралельному регіоні

#pragma omp parallel
    {
        printf("The parallel region is executed by thread %d\n", omp_get_thread_num());
    }
    return 0;
}