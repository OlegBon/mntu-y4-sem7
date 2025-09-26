// Тут omp_get_num_threads() викликається вже після завершення паралельної області,
// тобто в послідовному коді, де працює лише головний потік.
// Тому результат завжди буде 1, незалежно від того, скільки потоків було в паралельному блоці.

//#include <omp.h>
//#include <stdio.h>
//
//int main()
//{
//    omp_set_num_threads(8); // Встановлюємо бажану кількість потоків
//
//#pragma omp parallel
//    {
//        printf("Thread %d is executing\n", omp_get_thread_num());
//    }
//    printf("\nTotal threads: %d\n", omp_get_num_threads());
//
//    return 0;
//}

// А тут omp_get_num_threads() викликається всередині паралельної області,
// і ми обмежуємо вивід лише потоком 0, щоб уникнути дублювання.
// Це правильний спосіб дізнатися кількість активних потоків.

#include <omp.h>
#include <stdio.h>

int main()
{
    omp_set_num_threads(8); // Встановлюємо бажану кількість потоків

#pragma omp parallel
    {
        printf("Thread %d is executing\n", omp_get_thread_num());

        // Вивід кількості потоків зсередини паралельної області
        if (omp_get_thread_num() == 0) {
            printf("Total threads: %d\n", omp_get_num_threads());
        }
    }

    return 0;
}