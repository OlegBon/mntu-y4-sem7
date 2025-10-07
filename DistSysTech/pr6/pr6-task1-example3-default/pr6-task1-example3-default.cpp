#include <stdio.h>
#include <omp.h>

int main() {
    int n = 6; // Кількість ітерацій
    int i, a, b, c; // Лічильник і змінні

#pragma omp parallel default(shared) private(a, b, c)
    {
#pragma omp for
        for (i = 0; i < n; i++) {
            a = i + 1;
            b = i * 2;
            c = a + b;
            printf("Thread %d: a = %d, b = %d, c = %d, i = %d\n",
                omp_get_thread_num(), a, b, c, i);
        }
    }

    return 0;
}