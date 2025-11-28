using System;
using System.Threading;

namespace PR14_Task1
{
    class PR14_Task1
    {
        // Глобальні змінні (x = номер варіанту = 1)
        static int x = 1;
        static int y = 5;
        //static int z = 4;

        // Семафори для управління стрілками графа
        static Semaphore S1 = new Semaphore(0, 1); // Стрілка T1 -> T3
        static Semaphore S2 = new Semaphore(0, 1); // Стрілка T2 -> T4
        static Semaphore S3 = new Semaphore(0, 1); // Стрілка T3 -> T5
        static Semaphore S4 = new Semaphore(0, 1); // Стрілка T4 -> T5

        static void Main(string[] args)
        {
            //Console.WriteLine($"Initial data: x={x}, y={y}, z={z}\n");
            Console.WriteLine($"Initial data: x={x}, y={y}\n");

            // Створення потоків
            Thread T1 = new Thread(Func_T1);
            Thread T2 = new Thread(Func_T2);
            Thread T3 = new Thread(Func_T3);
            Thread T4 = new Thread(Func_T4);
            Thread T5 = new Thread(Func_T5);

            // Запуск потоків
            // Порядок запуску не важливий, семафори все синхронізують
            T1.Start();
            T2.Start();
            T3.Start();
            T4.Start();
            T5.Start();

            // Очікування завершення фінального потоку T5
            T5.Join();

            // Очікування інших
            // (про всяк випадок, хоча логічно вони завершаться раніше T5)
            T1.Join(); T2.Join(); T3.Join(); T4.Join();

            Console.WriteLine("\nAll streams have finished working.");
        }

        // Логіка потоків
        static void Func_T1()
        {
            // x = x * 5
            x = x * 5;
            Console.WriteLine($"[T1] x = x * 5, x={x}");

            // Відкриваємо шлях для T3
            S1.Release();
        }

        static void Func_T2()
        {
            // y = y + 2
            y = y + 2;
            Console.WriteLine($"[T2] y = y + 2, y={y}");

            // Відкриваємо шлях для T4
            S2.Release();
        }

        static void Func_T3()
        {
            // Чекаємо завершення T1
            S1.WaitOne();

            // x = x + 2
            x = x + 2;
            Console.WriteLine($"[T3] x = x + 2, x={x}");

            // Відкриваємо шлях для T5
            S3.Release();
        }

        static void Func_T4()
        {
            // Чекаємо завершення T2
            S2.WaitOne();

            // y = y - 3
            y = y - 3;
            Console.WriteLine($"[T4] y = y - 3, y={y}");

            // Відкриваємо шлях для T5
            S4.Release();
        }

        static void Func_T5()
        {
            // Чекаємо завершення T3 та T4
            S3.WaitOne();
            S4.WaitOne();

            // y = x * y
            y = x * y;
            Console.WriteLine($"[T5] y = x * y, y={y}");

            Console.WriteLine("------------------------");
            Console.WriteLine($"Final result: x={x}, y={y}");
        }
    }
}