#include <stdio.h>
#include <omp.h>

int main() {
    int i, n = 100, chunk = 10;
    float a[100], b[100], result = 0.0;

    // Ініціалізація масивів
    for (i = 0; i < n; i++) {
        a[i] = i * 1.0;
        b[i] = i * 2.0;
    }

    // Паралельне обчислення скалярного добутку з REDUCTION
#pragma omp parallel for default(shared) private(i) schedule(static, chunk) reduction(+:result)
    for (i = 0; i < n; i++) {
        result += a[i] * b[i];
    }

    // Вивід фінального результату
    printf("Final result = %f\n", result);

    return 0;
}