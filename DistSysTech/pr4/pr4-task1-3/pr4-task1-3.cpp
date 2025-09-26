#include <omp.h>
#include <stdio.h>

int main()
{
    omp_set_dynamic(0); // Вимкнути динамічну зміну кількості потоків
    omp_set_num_threads(12); // Встановити глобальну кількість потоків

#pragma omp parallel num_threads(6)
    {
        printf("Thread %d is active\n", omp_get_thread_num());
    }
    return 0;
}