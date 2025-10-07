#include <stdio.h>
#include <omp.h>

int main() {
    int n = 6;
    int i, a;

#pragma omp parallel for private(i) lastprivate(a)
    for (i = 0; i < n; i++) {
        a = i + 1;
        printf("Thread %d has a value of a = %d for i = %d\n",
            omp_get_thread_num(), a, i);
    }

    // Значення змінної a після завершення паралельного циклу
    printf("Value of a after parallel for: a = %d\n", a);

    return 0;
}