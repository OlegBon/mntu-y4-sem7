using System;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;

namespace pr1
{
    public partial class Form1 : Form
    {
        // Внутрішні змінні
        int[] array = null!;// масив-оригінал, null - початкове значення
        int[] arrayBub = null!;// масив даних після сортування бульбашкою
        int[] arrayIns = null!;// масив після сортуванням вставкою
        int[] arraySel = null!;// масив після сортування вибором

        // Змінні, що фіксують час початку виконання алгоритмів
        TimeSpan tsBubble;// Алгоритм бульбашки
        TimeSpan tsIns;// Вставка
        TimeSpan tsSel;// Вибір
        bool fCancelBub;// Якщо true, то була натиснута кнопка Stop – зупинити всі потоки
        bool fCancelIns;
        bool fCancelSel;

        public Form1()
        {
            InitializeComponent();

            // Очистити поле textBox1
            textBox1.Text = "";

            // Очистити ListBox
            listBox1.Items.Clear();
            listBox2.Items.Clear();
            listBox3.Items.Clear();

            // Очистити ProgressBar
            progressBar1.Value = 0;
            progressBar2.Value = 0;
            progressBar3.Value = 0;

            // Деактивувати деякі елементи керування
            Active(false);

            // Налаштувати внутрішні змінні
            fCancelBub = false;
            fCancelIns = false;
            fCancelSel = false;
        }

        // Внутрішній метод, який відображає масив елемента управління типу ListBox
        private void DisplayArray(int[] A, ListBox LB)
        {
            LB.Items.Clear();
            for (int i = 0; i < A.Length; i++)
                LB.Items.Add(A[i]);
        }

        // Внутрішній метод активації елементів керування
        private void Active(bool active)
        {
            // Зробити активними/неактивними деякі елементи управління
            label2.Enabled = active;
            label3.Enabled = active;
            label4.Enabled = active;
            label5.Enabled = active;
            label6.Enabled = active;
            label7.Enabled = active;
            listBox1.Enabled = active;
            listBox2.Enabled = active;
            listBox3.Enabled = active;
            progressBar1.Enabled = active;
            progressBar2.Enabled = active;
            progressBar3.Enabled = active;
            button2.Enabled = active;
            button3.Enabled = active;
        }

        // Кнопка "Generate array"
        private void button1_Click(object sender, EventArgs e)
        {
            // Деактивувати деякі елементи керування
            Active(false);

            // Налаштувати мітки
            label5.Text = "";
            label6.Text = "";
            label7.Text = "";

            // Запустити генерування масиву в потоці
            if (!backgroundWorker1.IsBusy)
                backgroundWorker1.RunWorkerAsync();// згенерувати подію DoWork
        }

        // Кнопка "Sort" - запустити потоки виконання
        private void button2_Click(object sender, EventArgs e)
        {
            // Деактивувати кнопку генерування масиву
            button1.Enabled = false;

            // Запуск методів сортування у потоках
            if (!backgroundWorker2.IsBusy)
                backgroundWorker2.RunWorkerAsync();
            if (!backgroundWorker3.IsBusy)
                backgroundWorker3.RunWorkerAsync();
            if (!backgroundWorker4.IsBusy)
                backgroundWorker4.RunWorkerAsync();
        }

        // Кнопка Stop – скасувати виконання всіх потоків
        private void button3_Click(object sender, EventArgs e)
        {
            try
            {
                backgroundWorker2.CancelAsync();// зупинити сортування бульбашкою
                backgroundWorker3.CancelAsync();// Зупинити сортування вставками
                backgroundWorker4.CancelAsync();// зупинити сортування вибором
            }
            catch (InvalidOperationException ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        // Виконання потоку, у якому генерується масив чисел
        private void backgroundWorker1_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. Оголошення внутрішніх змінних
            Random rnd = new Random();

            // 2. Отримати кількість елементів у масиві
            int n = Convert.ToInt32(textBox1.Text);
            
            // 3. Виділити пам'ять для масивів та заповнити їх значеннями
            array = new int[n];
            arrayBub = new int[n];
            arrayIns = new int[n];
            arraySel = new int[n];
            for (int i = 0; i < n; i++)
            {
                Thread.Sleep(1);
                array[i] = rnd.Next(1, n + 1);// випадкове число
                arrayBub[i] = arraySel[i] = arrayIns[i] = array[i];// скопіювати це число
                
                // Викликати відображення прогресу (зміни) виконання потоку
                try
                {
                    backgroundWorker1.ReportProgress((i * 100) / n);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }
            }
        }

        // Сортування методом бульбашки – потік
        private void backgroundWorker2_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // Сортується масив arrayBub
            int x;

            // Ініціалізувати час
            tsBubble = new TimeSpan(DateTime.Now.Ticks);
            for (int i = 0; i < arrayBub.Length; i++)
            {
                Thread.Sleep(1);// дати можливість іншим потокам виконуватись паралельно
                for (int j = arrayBub.Length - 1; j > i; j--)
                {
                    if (arrayBub[j - 1] > arrayBub[j])// Сортування за зростанням
                    {
                        x = arrayBub[j];
                        arrayBub[j] = arrayBub[j - 1];
                        arrayBub[j - 1] = x;
                    }
                }
                
                // Відобразити зміну прогресу
                try
                {
                    backgroundWorker2.ReportProgress((i * 100) / arrayBub.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }

                // Перевірка, чи зупинено потік
                if (backgroundWorker2.CancellationPending)
                {
                    fCancelBub = true;
                    break;
                }
            }
        }

        // Сортування вставками
        private void backgroundWorker3_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. Оголосити внутрішні перемінні
            int x, i, j;

            // Ініціалізувати час
            tsIns = new TimeSpan(DateTime.Now.Ticks);

            // 2. Цикл сортування
            for (i = 0; i < arrayIns.Length; i++)
            {

                // дати можливість іншим потокам виконуватись паралельно
                Thread.Sleep(1);
                x = arrayIns[i];

                // Пошук місця елемента у послідовності
                for (j = i - 1; j >= 0 && arrayIns[j] > x; j--)
                    arrayIns[j + 1] = arrayIns[j];// зрушити елемент праворуч
                arrayIns[j + 1] = x;

                // Відобразити зміну прогресу
                try
                {
                    backgroundWorker3.ReportProgress((i * 100) / arrayIns.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }

                // Перевірка, чи зупинено потік
                if (backgroundWorker3.CancellationPending)
                {
                    fCancelIns = true;
                    break;
                }
            }
        }

        // Сортування вибором
        private void backgroundWorker4_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. Оголосити змінні
            int i, j, k;
            int x;

            // 2. Встановити початковий час
            tsSel = new TimeSpan(DateTime.Now.Ticks);

            // 3. Цикл сортування вибором
            for (i = 0; i < arraySel.Length; i++)
            {
                
                // дати можливість іншим потокам виконуватись паралельно
                Thread.Sleep(1);
                k = i;
                
                // Пошук найменшого елемента
                x = arraySel[i];
                for (j = i + 1; j < arraySel.Length; j++)
                    if (arraySel[j] < x)
                    {
                        k = j;// k – індекс найменшого елемента
                        x = arraySel[j];
                    }
                
                // Поміняти місцями найменший елемент з arraySel[i]
                arraySel[k] = arraySel[i];
                arraySel[i] = x;
                
                // Відобразити зміну прогресу
                try
                {
                    backgroundWorker4.ReportProgress((i * 100) / arraySel.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }
                
                // Перевірка, чи зупинено потік
                if (backgroundWorker4.CancellationPending)
                {
                    fCancelSel = true;
                    break;
                }
            }
        }

        // Зміна (прогрес) виконаної роботи в потоці генерування масиву
        private void backgroundWorker1_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            // Відобразити зміну тексту кнопки "Generate array"
            //button1.Text = "Generate array" + e.ProgressPercentage.ToString() + "%";
            button1.Text = $"Generate array [{e.ProgressPercentage}%]";

        }

        // Зміна прогресу у методі сортування бульбашкою
        private void backgroundWorker2_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label5.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar1.Value = e.ProgressPercentage;
        }

        // Прогрес для методу сортування вставками
        private void backgroundWorker3_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label6.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar2.Value = e.ProgressPercentage;
        }

        // Зміна прогресу для алгоритму сортування вибором
        private void backgroundWorker4_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label7.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar3.Value = e.ProgressPercentage;
        }

        // Дії після завершення потоку, що генерує масив чисел
        private void backgroundWorker1_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // Після того, як масив згенерований, зробити відповідні налаштування
            button1.Text = "Generate array";
            
            // Зробити активними видимі елементи керування
            Active(true);
            
            // Відобразити масив-оригінал в елементах керування типу ListBox
            DisplayArray(array, listBox1);
            DisplayArray(array, listBox2);
            DisplayArray(array, listBox3);
        }

        // Завершення сортування методом пляшечки - виконати кінцеві операції
        private void backgroundWorker2_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // Якщо було скасування сортування
            if (fCancelBub)
            {
                // Налаштувати відповідно елементи керування
                label5.Text = "";
                
                // Відобразити масив-оригінал
                DisplayArray(array, listBox1);
                fCancelBub = false;
            }
            else
            {
                // Зафіксувати час та вивести його
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsBubble;
                label5.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // Відобразити відсортований масив
                DisplayArray(arrayBub, listBox1);
            }
            
            // Налаштувати інші елементи керування
            progressBar1.Value = 0;
            button1.Enabled = true;
        }

        // Завершення потоку сортування вставками
        private void backgroundWorker3_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // Якщо було скасування сортування
            if (fCancelIns)
            {
                // Налаштувати відповідно елементи керування
                label6.Text = "";
                
                // Відобразити масив-оригінал
                DisplayArray(array, listBox2);
                fCancelIns = false;
            }
            else
            {
                // Зафіксувати час та вивести його
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsIns;
                label6.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // Відобразити відсортований масив
                DisplayArray(arrayIns, listBox2);
            }
            // Налаштувати інші елементи керування
            progressBar2.Value = 0;
            button1.Enabled = true;
        }

        // Завершення сортування вибором
        private void backgroundWorker4_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // Якщо було скасування сортування
            if (fCancelSel)
            {
                // Налаштувати відповідно елементи керування
                label7.Text = "";
                
                // Відобразити масив-оригінал
                DisplayArray(array, listBox3);
                fCancelSel = false;
            }
            else
            {
                // Зафіксувати час та вивести його
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsSel;
                label7.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // Відобразити відсортований масив
                DisplayArray(arraySel, listBox3);
            }
            // Налаштувати інші елементи керування
            progressBar3.Value = 0;
            button1.Enabled = true;
        }
    }
}
