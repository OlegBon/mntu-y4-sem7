using System;
using System.Threading;

namespace PR13_Task3
{
    // Клас для виконання обчислень у потоці
    class Calculator
    {
        private double[] _vector;
        private string _name;
        public double Result { get; private set; }

        public Calculator(double[] vector, string name)
        {
            _vector = vector;
            _name = name;
        }

        // Метод для обчислення виразу A (для потоку T0)
        // Формула: Sum(cbrt(x * sin(x^2)))
        public void CalculateA()
        {
            Console.WriteLine($"[{_name}] Start of calculations (Priority: {Thread.CurrentThread.Priority})");

            double sum = 0;

            // Штучне навантаження для Візуалізатора паралелізму (щоб потік жив довше)
            // У реальному житті цей цикл не потрібен, якщо N велике.
            for (int k = 0; k < 10_000_000; k++)
            {
                sum = 0; // Скидаємо суму для імітації довгого процесу
                for (int i = 0; i < _vector.Length; i++)
                {
                    double x = _vector[i];
                    // Math.Cbrt - кубічний корінь
                    // x * x - це x у квадраті
                    sum += Math.Cbrt(x * Math.Sin(x * x));
                }
            }

            Result = sum;
            Console.WriteLine($"[{_name}] Completed.");
        }

        // Метод для обчислення виразу B (для потоку T1)
        // Формула: Sum(cbrt(y * cos(y^2)))
        public void CalculateB()
        {
            Console.WriteLine($"[{_name}] Start of calculations (Priority: {Thread.CurrentThread.Priority})");

            double sum = 0;

            // Штучне навантаження
            for (int k = 0; k < 10_000_000; k++) // Для наваетаження, щоб довше працювало
            {
                sum = 0;
                for (int i = 0; i < _vector.Length; i++)
                {
                    double y = _vector[i];
                    sum += Math.Cbrt(y * Math.Cos(y * y));
                }
            }

            Result = sum;
            Console.WriteLine($"[{_name}] Completed.");
        }
    }

    class PR13_Task3
    {
        static void Main(string[] args)
        {
            // Ініціалізація даних (головний потік)
            int Nx = 10;
            int Ny = 15;
            //int Ny = 10;
            double[] X = new double[Nx];
            double[] Y = new double[Ny];
            Random rand = new Random();

            Console.WriteLine("Generation of vectors");

            // Заповнення X: [0..25]
            Console.Write("Vector X: ");
            for (int i = 0; i < Nx; i++)
            {
                X[i] = rand.NextDouble() * 25;
                Console.Write($"{X[i]:F2} ");
            }
            Console.WriteLine("\n");

            // Заповнення Y: [-10..10]
            // rand.NextDouble() дає [0..1].
            // * 20 дає [0..20].
            // - 10 дає [-10..10].
            Console.Write("Vector Y: ");
            for (int i = 0; i < Ny; i++)
            {
                Y[i] = rand.NextDouble() * 20 - 10;
                Console.Write($"{Y[i]:F2} ");
            }
            Console.WriteLine("\n\nStream preparation");

            // Створення об'єктів-калькуляторів
            Calculator calcA = new Calculator(X, "T0");
            Calculator calcB = new Calculator(Y, "T1");

            // Створення потоків
            Thread T0 = new Thread(calcA.CalculateA);
            Thread T1 = new Thread(calcB.CalculateB);

            // Налаштування імен та пріоритетів (Згідно завдання)
            T0.Name = "T0_Lowest";
            T0.Priority = ThreadPriority.Lowest; // Найнижчий

            T1.Name = "T1_BelowNormal";
            T1.Priority = ThreadPriority.BelowNormal; // Нижче нормального

            // Запуск
            // Спочатку запускаємо T1 (вищий пріоритет), потім T0, або одночасно.
            // Планувальник сам вирішить, кому дати ресурси.
            T1.Start();
            T0.Start();

            Console.WriteLine("Streams are running. Main stream is waiting.");

            // Очікування завершення
            T1.Join();
            T0.Join();

            // Вивід результатів
            Console.WriteLine("\n\nResults");
            Console.WriteLine($"Result A (T0): {calcA.Result:F4}");
            Console.WriteLine($"Result B (T1): {calcB.Result:F4}");

        }
    }
}