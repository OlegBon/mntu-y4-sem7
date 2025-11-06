package DistSysTech.pr10;

// Монітор для синхронізації потоків
class Data {
    // Спільні ресурси
    final int N = 1000; // Розмір матриць (N x N)
    final int P = 4; // Кількість потоків
    final int H = N / P; // Розмір порції для кожного потоку

    // Матриці (спільні ресурси)
    double[][] A = new double[N][N];
    double[][] B = new double[N][N];
    double[][] C = new double[N][N];
    double[][] MZ = new double[N][N];

    // Змінні синхронізації (лічильники)
    private int f_in = 0; // Лічильник сигналів "Введення завершено"
    private int f_out = 0; // Лічильник сигналів "Обчислення завершено"

    // Потоки P2, P3, P4 чекають, поки f_in не стане 3
    // (тобто, поки P1 не подасть 3 сигнали)
    public synchronized void wait_In() {
        try {
            while (f_in < 3) {
                wait(); // Потік "засинає" і звільняє монітор
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // P1 викликає цей метод 3 рази, щоб "розбудити" P2, P3, P4
    public synchronized void Signal_In() {
        f_in++;
        // 'notifyAll' гарантує, що всі потоки, які чекають, прокинуться
        // і перевірять умову 'while' у wait_In()
        notifyAll();
    }

    // P1 чекає, поки f_out не стане 3
    // (тобто, поки P2, P3, P4 не подадуть 3 сигнали).
    public synchronized void wait_Out() {
        try {
            while (f_out < 3) {
                wait(); // P1 "засинає" і звільняє монітор
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // P2, P3, P4 викликають цей метод, щоб "розбудити" P1
    public synchronized void Signal_Out() {
        f_out++;
        // 'notify' достатньо, оскільки ми знаємо, що чекає лише P1
        notify();
    }
}

// Алгоритм роботи процесу P1
class Thread1 extends Thread {
    private Data d; // Посилання на спільний монітор

    public Thread1(Data d) {
        this.d = d;
    }

    @Override
    public void run() {
        // 1. Ввід B, C, MZ (симулюємо заповненням)
        for (int i = 0; i < d.N; i++) {
            for (int j = 0; j < d.N; j++) {
                d.B[i][j] = 1.0;
                d.C[i][j] = 2.0;
                d.MZ[i][j] = 3.0;
            }
        }
        System.out.println("P1: Data input finished.");

        // 2-4. Signal_In (повідомляємо іншим, що дані готові)
        d.Signal_In(); // для P2
        d.Signal_In(); // для P3
        d.Signal_In(); // для P4

        // 5. Обчислення своєї порції (H1: 0 -> H)
        int H = d.H;
        for (int i = 0; i < H; i++) {
            for (int j = 0; j < d.N; j++) {
                double sum = 0;
                for (int k = 0; k < d.N; k++) {
                    sum += d.C[i][k] * d.MZ[k][j]; // C[i,k] * MZ[k,j]
                }
                d.A[i][j] = d.B[i][j] + sum;
            }
        }
        System.out.println("P1: Calculation finished.");

        // 6-8. wait_Out (чекаємо на P2, P3, P4)
        d.wait_Out();
        d.wait_Out();
        d.wait_Out();

        // 9. Вивід A (виведемо один елемент для перевірки)
        System.out.println("P1: All threads finished.");
        System.out.println("Result A[0][0] = " + d.A[0][0]);
        System.out.println("Result A[N-1][N-1] = " + d.A[d.N - 1][d.N - 1]);
    }
}

// Алгоритм роботи процесу P2
class Thread2 extends Thread {
    private Data d;

    public Thread2(Data d) {
        this.d = d;
    }

    @Override
    public void run() {
        // 1. Чекати сигнал (ввід)
        d.wait_In();
        System.out.println("P2: Started calculation.");

        // 2. Обчислення своєї порції (H2: H -> 2*H)
        int H = d.H;
        for (int i = H; i < 2 * H; i++) {
            for (int j = 0; j < d.N; j++) {
                double sum = 0;
                for (int k = 0; k < d.N; k++) {
                    sum += d.C[i][k] * d.MZ[k][j];
                }
                d.A[i][j] = d.B[i][j] + sum;
            }
        }

        // 3. Сигнал (вихід)
        System.out.println("P2: Calculation finished.");
        d.Signal_Out();
    }
}

// Алгоритм роботи процесу P3
class Thread3 extends Thread {
    private Data d;

    public Thread3(Data d) {
        this.d = d;
    }

    @Override
    public void run() {
        // 1. Чекати сигнал (ввід)
        d.wait_In();
        System.out.println("P3: Started calculation.");

        // 2. Обчислення своєї порції (H3: 2*H -> 3*H)
        int H = d.H;
        for (int i = 2 * H; i < 3 * H; i++) {
            for (int j = 0; j < d.N; j++) {
                double sum = 0;
                for (int k = 0; k < d.N; k++) {
                    sum += d.C[i][k] * d.MZ[k][j];
                }
                d.A[i][j] = d.B[i][j] + sum;
            }
        }

        // 3. Сигнал (вихід)
        System.out.println("P3: Calculation finished.");
        d.Signal_Out();
    }
}

// Алгоритм роботи процесу P4
class Thread4 extends Thread {
    private Data d;

    public Thread4(Data d) {
        this.d = d;
    }

    @Override
    public void run() {
        // 1. Чекати сигнал (ввід)
        d.wait_In();
        System.out.println("P4: Started calculation.");

        // 2. Обчислення своєї порції (H4: 3*H -> N)
        // (Беремо до d.N, щоб врахувати залишок, якщо N не ділиться на 4)
        int H = d.H;
        for (int i = 3 * H; i < d.N; i++) {
            for (int j = 0; j < d.N; j++) {
                double sum = 0;
                for (int k = 0; k < d.N; k++) {
                    sum += d.C[i][k] * d.MZ[k][j];
                }
                d.A[i][j] = d.B[i][j] + sum;
            }
        }

        // 3. Сигнал (вихід)
        System.out.println("P4: Calculation finished.");
        d.Signal_Out();
    }
}

// Головний клас для запуску програми
public class MainClass {
    public static void main(String[] args) {
        // Створюємо монітор (один для всіх потоків)
        Data monitor = new Data();

        // Створюємо 4 потоки, передаючи їм той самий монітор
        Thread1 p1 = new Thread1(monitor);
        Thread2 p2 = new Thread2(monitor);
        Thread3 p3 = new Thread3(monitor);
        Thread4 p4 = new Thread4(monitor);

        System.out.println("Starting all 4 threads...");
        // Запускаємо потоки
        p1.start();
        p2.start();
        p3.start();
        p4.start();
    }
}