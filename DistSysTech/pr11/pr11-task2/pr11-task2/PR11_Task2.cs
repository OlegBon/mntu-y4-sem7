using System;
using System.Threading;

namespace Lab1_Task2
{
    // Клас для обчислень суми та добутку елементів масиву
    public class ArrayCalculator
    {
        private int[] _array;

        // Поля для зберігання результатів обчислень
        private long _sumResult;
        private long _productResult; // 'long' щоб уникнути переповнення

        public ArrayCalculator(int[] array)
        {
            this._array = array;
        }

        // Метод для Потоку T0
        public void FindSum()
        {
            long sum = 0;
            for (int i = 0; i < _array.Length; i++)
            {
                sum += _array[i];
                // Додамо невелику паузу
                Thread.Sleep(50);
            }
            _sumResult = sum; // Зберігаємо результат у спільному полі
            Console.WriteLine($"\n[T0] The amount is calculated: {_sumResult}");
        }

        // Метод для Потоку T1
        public void FindProduct()
        {
            long product = 1;
            for (int i = 0; i < _array.Length; i++)
            {
                // Якщо хоча б один елемент 0, добуток завжди 0
                if (_array[i] == 0)
                {
                    product = 0;
                    break;
                }
                product *= _array[i];
                // "Спимо"
                Thread.Sleep(50);
            }
            _productResult = product; // Зберігаємо результат
            Console.WriteLine($"\n[T1] The product is calculated: {_productResult}");
        }

        // Методи для безпечного отримання результатів (після Join)
        public long GetSum() { return _sumResult; }
        public long GetProduct() { return _productResult; }
    }

    class PR11_Task2
    {
        static void Main(string[] args)
        {
            // Створюємо та ініціалізуємо масив
            int[] sharedArray = new int[10];
            Random rand = new Random();
            Console.WriteLine("Generated array (10 numbers, 0..25):");
            for (int i = 0; i < sharedArray.Length; i++)
            {
                sharedArray[i] = rand.Next(0, 26); // 0..25
                Console.Write(sharedArray[i] + " ");
            }
            Console.WriteLine("\n\nRun streams T0 (Sum) and T1 (Product)");

            // Створюємо екземпляр калькулятора зі спільним масивом
            ArrayCalculator calculator = new ArrayCalculator(sharedArray);

            // Створюємо потоки
            // T0 буде виконувати FindSum() на об'єкті 'calculator'
            Thread T0 = new Thread(calculator.FindSum);

            // T1 буде виконувати FindProduct() на тому ж об'єкті 'calculator'
            Thread T1 = new Thread(calculator.FindProduct);

            // Запускаємо потоки
            T0.Start();
            T1.Start();

            // Очікуємо завершення обох потоків 
            Console.WriteLine("The main stream is waiting for T0 and T1 to complete");
            T0.Join(); // Головний потік "засинає", поки T0 не завершиться
            T1.Join(); // Головний потік "засинає", поки T1 не завершиться

            // Отримаємо результати (це безпечно, бо потоки вже завершились)
            Console.WriteLine("\nBoth streams have finished working");
            Console.WriteLine($"  > Result T0 (Amount):   {calculator.GetSum()}");
            Console.WriteLine($"  > Result T1 (Product): {calculator.GetProduct()}");

        }
    }
}