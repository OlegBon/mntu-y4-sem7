using System;
using System.Threading;

namespace Lab1_Task1
{
    class Program
    {
        private static readonly Random rand = new Random();

        // Об'єкт для блокування доступу до Random
        private static readonly object randLocker = new object();

        static void Main(string[] args)
        {
            Console.WriteLine("Run streams T0 and T1:");

            // Створюємо потік T0 і кажемо йому виконати метод Func_T0
            Thread T0 = new Thread(Func_T0);

            // Створюємо потік T1 і кажемо йому виконати метод Func_T1
            Thread T1 = new Thread(Func_T1);

            T0.Start();
            T1.Start();

            // Метод Join() блокує головний потік, 
            // доки T0 не завершить свою роботу.
            T0.Join();

            // Чекаємо на T1
            T1.Join();
        }

        // Вивід логіки для потоку T0: 10 випадкових чисел від 0 до 100
        static void Func_T0()
        {
            for (int i = 0; i < 10; i++)
            {
                int num;

                // Захоплюємо замок, щоб безпечно отримати випадкове число
                lock (randLocker)
                {
                    num = rand.Next(0, 101);
                }

                Console.Write($"T0[{num}]\n");

                // "Спимо" 100мс, щоб дати шанс іншому потоку попрацювати
                Thread.Sleep(100);
            }
        }

        // Вивід логіки для потоку T1: 20 випадкових літер англійського алфавіту
        static void Func_T1()
        {
            for (int i = 0; i < 20; i++)
            {
                char letter;

                // Захоплюємо замок, щоб безпечно отримати випадкове число
                lock (randLocker)
                {
                    letter = (char)('A' + rand.Next(0, 26));
                }

                Console.Write($"T1[{letter}]\n");

                // "Спимо" 50мс (трохи швидше, ніж T0)
                Thread.Sleep(50);
            }
        }
    }
}