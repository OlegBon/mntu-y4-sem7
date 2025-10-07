#include <stdio.h>
#include <omp.h>

int main() {
    int i, n = 100;
    float a[100], sum = 0.0;

    // Ініціалізація масиву
    for (i = 0; i < n; i++) {
        a[i] = i + 1.0;
    }

    // Паралельне обчислення суми з REDUCTION
#pragma omp parallel for reduction(+:sum)
    for (i = 0; i < n; i++) {
        sum += a[i];
    }

    // Вивід результату
    printf("Max threads available: %d\n", omp_get_max_threads());
    printf("Sum of array elements = %f\n", sum);

    return 0;
}