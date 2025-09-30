#include <omp.h>
#include <stdio.h>

int main()
{
    int n = 20; // Кількість ітерацій
    int i;

    omp_set_num_threads(4); // Встановлюємо 4 потоки

#pragma omp parallel shared(n) private(i)
    {
#pragma omp for
        for (i = 0; i < n; i++)
        {
            printf("Thread %d processes iteration %d\n", omp_get_thread_num(), i);
        }
    }

    return 0;
}