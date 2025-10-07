#include <stdio.h>
#include <omp.h>

int main() {
    int i, n = 100;
    float a[100], sum = 0.0;

    // Ініціалізація масиву
    for (i = 0; i < n; i++) {
        a[i] = i + 1.0;
    }

	omp_set_num_threads(6); // Встановлення кількості потоків

    // Паралельне обчислення суми з виводом TID і часткових сум
#pragma omp parallel reduction(+:sum)
    {
        int TID = omp_get_thread_num();
        float local_sum = 0.0;

#pragma omp for
        for (i = 0; i < n; i++) {
            local_sum += a[i];
        }

        printf("Thread %d computed local sum = %.2f\n", TID, local_sum);
        sum += local_sum; // Це вже обробляється reduction, залишемо для демонстрації
    }

    // Глобальний результат
    printf("Final global sum = %.2f\n", sum);

    return 0;
}