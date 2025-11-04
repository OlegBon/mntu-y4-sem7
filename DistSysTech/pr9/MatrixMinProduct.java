package DistSysTech.pr9;

import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

// Клас для зберігання результату пари рядків
// (мінімальний добуток та індекси рядків)
class PairResult {
    double minProduct = Double.MAX_VALUE; // Мінімальний скалярний добуток
    int bestRowI = -1; // Індекс першого рядка
    int bestRowJ = -1; // Індекс другого рядка

    public PairResult(double minProduct, int bestRowI, int bestRowJ) {
        this.minProduct = minProduct;
        this.bestRowI = bestRowI;
        this.bestRowJ = bestRowJ;
    }
}

// Клас, який реалізує пошук мінімального скалярного добутку
// для певного діапазону рядків матриці
class ProductFinder implements Runnable {
    private final double[][] matrix;
    private final int i_start; // Початковий рядок (включно)
    private final int i_end; // Кінцевий рядок (виключно)
    private final int m; // Загальна кількість рядків
    private final int n; // Загальна кількість стовпців

    private PairResult localResult; // Результат цього потоку

    public ProductFinder(double[][] matrix, int i_start, int i_end) {
        this.matrix = matrix;
        this.i_start = i_start;
        this.i_end = i_end;
        this.m = matrix.length;
        this.n = matrix[0].length;
    }

    @Override
    public void run() {
        double localMinProd = Double.MAX_VALUE;
        int localBestI = -1;
        int localBestJ = -1;

        // Зовнішній цикл по рядках, призначених цьому потоку
        for (int i = i_start; i < i_end; i++) {
            // Внутрішній цикл по рядках, що йдуть після i
            // Щоб уникнути повторів (i, j та j, i) і самодобутку (i,i)
            for (int j = i + 1; j < m; j++) {

                // Обчислення скалярного добутку для пари (i, j)
                double currentProduct = 0;
                for (int k = 0; k < n; k++) {
                    currentProduct += matrix[i][k] * matrix[j][k];
                }

                // Перевірка, чи цей добуток - новий локальний мінімум
                if (currentProduct < localMinProd) {
                    localMinProd = currentProduct;
                    localBestI = i;
                    localBestJ = j;
                }
            }
        }

        // Зберігаємо результат роботи цього потоку
        this.localResult = new PairResult(localMinProd, localBestI, localBestJ);
    }

    // Повертає результат роботи потоку
    public PairResult getResult() {
        return localResult;
    }
}

// Головний клас для запуску програми
public class MatrixMinProduct {

    public static void main(String[] args) {
        // Налаштування матриці та потоків
        final int M_ROWS = 1000; // Кількість рядків (m)
        final int N_COLS = 2000; // Кількість стовпців (n)
        final int THREAD_COUNT = 6; // Кількість потоків (в мене 6-ядерний процесор та 12 логічних процесорів)

        // Генерація матриці розміром m x n з випадковими числами
        double[][] matrix = new double[M_ROWS][N_COLS];
        Random rand = ThreadLocalRandom.current();
        for (int i = 0; i < M_ROWS; i++) {
            for (int j = 0; j < N_COLS; j++) {
                matrix[i][j] = rand.nextDouble() * 20 - 10; // Випадкові числа від -10 до 10
            }
        }
        System.out.printf("Matrix %d x %d. Streams: %d\n", M_ROWS, N_COLS, THREAD_COUNT);

        // Виведення матриці
        // System.out.println("Matrix:");
        // for (int i = 0; i < M_ROWS; i++) {
        // for (int j = 0; j < N_COLS; j++) {
        // System.out.printf("%.2f ", matrix[i][j]);
        // }
        // System.out.println();
        // }

        // 1. Паралельне виконання
        System.out.println("Starting parallel mode...");
        ProductFinder[] finders = new ProductFinder[THREAD_COUNT];
        Thread[] threads = new Thread[THREAD_COUNT];
        int portionSize = M_ROWS / THREAD_COUNT; // Розмір "порції" рядків для потоку

        long startParallel = System.nanoTime();

        for (int i = 0; i < THREAD_COUNT; i++) {
            int from = i * portionSize;
            // Останній потік бере на себе "залишок", якщо m не ділиться націло
            int to = (i == THREAD_COUNT - 1) ? M_ROWS : (i + 1) * portionSize;

            finders[i] = new ProductFinder(matrix, from, to);
            threads[i] = new Thread(finders[i]);
            threads[i].start(); // Запускаємо потік
        }

        // Очікуємо завершення всіх потоків
        try {
            for (int i = 0; i < THREAD_COUNT; i++) {
                threads[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Збираємо результати
        // Знаходимо глобальний мінімальний добуток серед усіх потоків
        // і відповідні індекси рядків
        PairResult globalBest = new PairResult(Double.MAX_VALUE, -1, -1);
        for (int i = 0; i < THREAD_COUNT; i++) {
            PairResult local = finders[i].getResult();
            if (local.minProduct < globalBest.minProduct) {
                globalBest = local;
            }
        }

        long durationParallel = (System.nanoTime() - startParallel) / 1_000_000; // в мс

        System.out.printf("Parallel mode:\n\tA couple of lines: [%d, %d]\n\tProduct: %f\n\tTime: %d ms\n",
                globalBest.bestRowI, globalBest.bestRowJ, globalBest.minProduct, durationParallel);

        // 2. Послідовне виконання (для порівняння)
        System.out.println("Starting serial mode...");
        long startSerial = System.nanoTime();

        double serialMinProd = Double.MAX_VALUE;
        int serialBestI = -1;
        int serialBestJ = -1;

        for (int i = 0; i < M_ROWS; i++) {
            for (int j = i + 1; j < M_ROWS; j++) {
                // Обчислення скалярного добутку для пари (i, j)
                double currentProduct = 0;
                for (int k = 0; k < N_COLS; k++) {
                    currentProduct += matrix[i][k] * matrix[j][k];
                }
                if (currentProduct < serialMinProd) {
                    serialMinProd = currentProduct;
                    serialBestI = i;
                    serialBestJ = j;
                }
            }
        }

        long durationSerial = (System.nanoTime() - startSerial) / 1_000_000; // в мс

        System.out.printf("Sequential mode:\n\tA couple of lines: [%d, %d]\n\tProduct: %f\n\tTime: %d ms\n",
                serialBestI, serialBestJ, serialMinProd, durationSerial);

        // 3. Розрахунок прискорення
        System.out.printf("\nSpeed-up: %.2fx\n", (double) durationSerial / durationParallel);
    }
}