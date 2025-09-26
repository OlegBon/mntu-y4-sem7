#include <omp.h>
#include <stdio.h>

int main()
{
#pragma omp parallel
    {
        printf("The parallel region is executed by thread %d\n", omp_get_thread_num());
    }
    return 0;
}