#include <stdio.h>
#include <omp.h>

int main() {
    int vlen = 18; // Загальна довжина масиву
    int n = 6;     // Кількість ітерацій для кожного потоку
	int i, indx, TID; // Індекси та ідентифікатор потоку
    int a[18];     // Масив для запису результатів

    // Ініціалізація масиву
	// Спочатку маємо від -1 до -18
    for (i = 0; i < vlen; i++) {
        a[i] = -i - 1;
    }

    indx = 4; // Початкове значення, яке буде скопійовано кожному потоку

	omp_set_num_threads(2); // Обмеження кількості потоків до 2

#pragma omp parallel default(none) firstprivate(indx) private(i, TID) shared(n, a)

    {
		// Потік 0 та 1 отримає indx = 4. Будуть заповнені елементи з 4 по 9 та з 10 по 15
		// Кожен потік заповнить 6 елементів масиву a
        TID = omp_get_thread_num(); // Отримання ідентифікатора потоку
		// Для потоку 0: indx = 4 + 6 * 0 = 4
		// Для потоку 1: indx = 4 + 6 * 1 = 10
        indx += n * TID;
        for (i = indx; i < indx + n; i++) {
            a[i] = TID + 1;
        }
    }

    // Вивід результатів після паралельної області
    printf("After the parallel region:\n");
    for (i = 0; i < vlen; i++) {
        printf("a[%d] = %d\n", i, a[i]);
    }

    return 0;
}