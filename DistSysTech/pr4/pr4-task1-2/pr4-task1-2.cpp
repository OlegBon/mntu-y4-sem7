#include <omp.h>
#include <stdio.h>

int main()
{
#pragma omp parallel num_threads(6)
    {
        printf("Thread %d is working\n", omp_get_thread_num());
    }
return 0;
}