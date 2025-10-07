#include <stdio.h>
#include <omp.h>

int main() {
    int i, n = 6;

#pragma omp parallel
    {
        // Перша частина — цикл з nowait
#pragma omp for nowait
        for (i = 0; i < n; i++) {
            printf("Thread %d processing i = %d\n", omp_get_thread_num(), i);
        }

        // Друга частина — виконується одразу після циклу, без очікування інших потоків
        printf("Thread %d continues without waiting\n", omp_get_thread_num());
    }

    return 0;
}