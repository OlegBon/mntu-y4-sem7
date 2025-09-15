using System;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;

namespace pr1
{
    public partial class Form1 : Form
    {
        // ������� ����
        int[] array = null!;// �����-�������, null - ��������� ��������
        int[] arrayBub = null!;// ����� ����� ���� ���������� ����������
        int[] arrayIns = null!;// ����� ���� ����������� ��������
        int[] arraySel = null!;// ����� ���� ���������� �������

        // ����, �� �������� ��� ������� ��������� ���������
        TimeSpan tsBubble;// �������� ���������
        TimeSpan tsIns;// �������
        TimeSpan tsSel;// ����
        bool fCancelBub;// ���� true, �� ���� ��������� ������ Stop � �������� �� ������
        bool fCancelIns;
        bool fCancelSel;

        public Form1()
        {
            InitializeComponent();

            // �������� ���� textBox1
            textBox1.Text = "";

            // �������� ListBox
            listBox1.Items.Clear();
            listBox2.Items.Clear();
            listBox3.Items.Clear();

            // �������� ProgressBar
            progressBar1.Value = 0;
            progressBar2.Value = 0;
            progressBar3.Value = 0;

            // ������������ ���� �������� ���������
            Active(false);

            // ����������� ������� ����
            fCancelBub = false;
            fCancelIns = false;
            fCancelSel = false;
        }

        // �������� �����, ���� �������� ����� �������� ��������� ���� ListBox
        private void DisplayArray(int[] A, ListBox LB)
        {
            LB.Items.Clear();
            for (int i = 0; i < A.Length; i++)
                LB.Items.Add(A[i]);
        }

        // �������� ����� ��������� �������� ���������
        private void Active(bool active)
        {
            // ������� ���������/����������� ���� �������� ���������
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

        // ������ "Generate array"
        private void button1_Click(object sender, EventArgs e)
        {
            // ������������ ���� �������� ���������
            Active(false);

            // ����������� ����
            label5.Text = "";
            label6.Text = "";
            label7.Text = "";

            // ��������� ����������� ������ � ������
            if (!backgroundWorker1.IsBusy)
                backgroundWorker1.RunWorkerAsync();// ����������� ���� DoWork
        }

        // ������ "Sort" - ��������� ������ ���������
        private void button2_Click(object sender, EventArgs e)
        {
            // ������������ ������ ����������� ������
            button1.Enabled = false;

            // ������ ������ ���������� � �������
            if (!backgroundWorker2.IsBusy)
                backgroundWorker2.RunWorkerAsync();
            if (!backgroundWorker3.IsBusy)
                backgroundWorker3.RunWorkerAsync();
            if (!backgroundWorker4.IsBusy)
                backgroundWorker4.RunWorkerAsync();
        }

        // ������ Stop � ��������� ��������� ��� ������
        private void button3_Click(object sender, EventArgs e)
        {
            try
            {
                backgroundWorker2.CancelAsync();// �������� ���������� ����������
                backgroundWorker3.CancelAsync();// �������� ���������� ���������
                backgroundWorker4.CancelAsync();// �������� ���������� �������
            }
            catch (InvalidOperationException ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        // ��������� ������, � ����� ���������� ����� �����
        private void backgroundWorker1_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. ���������� �������� ������
            Random rnd = new Random();

            // 2. �������� ������� �������� � �����
            int n = Convert.ToInt32(textBox1.Text);
            
            // 3. ������� ���'��� ��� ������ �� ��������� �� ����������
            array = new int[n];
            arrayBub = new int[n];
            arrayIns = new int[n];
            arraySel = new int[n];
            for (int i = 0; i < n; i++)
            {
                Thread.Sleep(1);
                array[i] = rnd.Next(1, n + 1);// ��������� �����
                arrayBub[i] = arraySel[i] = arrayIns[i] = array[i];// ��������� �� �����
                
                // ��������� ����������� �������� (����) ��������� ������
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

        // ���������� ������� ��������� � ����
        private void backgroundWorker2_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // ��������� ����� arrayBub
            int x;

            // ������������ ���
            tsBubble = new TimeSpan(DateTime.Now.Ticks);
            for (int i = 0; i < arrayBub.Length; i++)
            {
                Thread.Sleep(1);// ���� ��������� ����� ������� ������������ ����������
                for (int j = arrayBub.Length - 1; j > i; j--)
                {
                    if (arrayBub[j - 1] > arrayBub[j])// ���������� �� ����������
                    {
                        x = arrayBub[j];
                        arrayBub[j] = arrayBub[j - 1];
                        arrayBub[j - 1] = x;
                    }
                }
                
                // ³��������� ���� ��������
                try
                {
                    backgroundWorker2.ReportProgress((i * 100) / arrayBub.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }

                // ��������, �� �������� ����
                if (backgroundWorker2.CancellationPending)
                {
                    fCancelBub = true;
                    break;
                }
            }
        }

        // ���������� ���������
        private void backgroundWorker3_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. ��������� ������� �������
            int x, i, j;

            // ������������ ���
            tsIns = new TimeSpan(DateTime.Now.Ticks);

            // 2. ���� ����������
            for (i = 0; i < arrayIns.Length; i++)
            {

                // ���� ��������� ����� ������� ������������ ����������
                Thread.Sleep(1);
                x = arrayIns[i];

                // ����� ���� �������� � �����������
                for (j = i - 1; j >= 0 && arrayIns[j] > x; j--)
                    arrayIns[j + 1] = arrayIns[j];// ������� ������� ��������
                arrayIns[j + 1] = x;

                // ³��������� ���� ��������
                try
                {
                    backgroundWorker3.ReportProgress((i * 100) / arrayIns.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }

                // ��������, �� �������� ����
                if (backgroundWorker3.CancellationPending)
                {
                    fCancelIns = true;
                    break;
                }
            }
        }

        // ���������� �������
        private void backgroundWorker4_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            // 1. ��������� ����
            int i, j, k;
            int x;

            // 2. ���������� ���������� ���
            tsSel = new TimeSpan(DateTime.Now.Ticks);

            // 3. ���� ���������� �������
            for (i = 0; i < arraySel.Length; i++)
            {
                
                // ���� ��������� ����� ������� ������������ ����������
                Thread.Sleep(1);
                k = i;
                
                // ����� ���������� ��������
                x = arraySel[i];
                for (j = i + 1; j < arraySel.Length; j++)
                    if (arraySel[j] < x)
                    {
                        k = j;// k � ������ ���������� ��������
                        x = arraySel[j];
                    }
                
                // ������� ������ ��������� ������� � arraySel[i]
                arraySel[k] = arraySel[i];
                arraySel[i] = x;
                
                // ³��������� ���� ��������
                try
                {
                    backgroundWorker4.ReportProgress((i * 100) / arraySel.Length);
                }
                catch (InvalidOperationException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }
                
                // ��������, �� �������� ����
                if (backgroundWorker4.CancellationPending)
                {
                    fCancelSel = true;
                    break;
                }
            }
        }

        // ���� (�������) �������� ������ � ������ ����������� ������
        private void backgroundWorker1_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            // ³��������� ���� ������ ������ "Generate array"
            //button1.Text = "Generate array" + e.ProgressPercentage.ToString() + "%";
            button1.Text = $"Generate array [{e.ProgressPercentage}%]";

        }

        // ���� �������� � ����� ���������� ����������
        private void backgroundWorker2_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label5.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar1.Value = e.ProgressPercentage;
        }

        // ������� ��� ������ ���������� ���������
        private void backgroundWorker3_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label6.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar2.Value = e.ProgressPercentage;
        }

        // ���� �������� ��� ��������� ���������� �������
        private void backgroundWorker4_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            label7.Text = Convert.ToString(e.ProgressPercentage) + "%";
            progressBar3.Value = e.ProgressPercentage;
        }

        // ĳ� ���� ���������� ������, �� ������ ����� �����
        private void backgroundWorker1_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // ϳ��� ����, �� ����� ������������, ������� ������� ������������
            button1.Text = "Generate array";
            
            // ������� ��������� ����� �������� ���������
            Active(true);
            
            // ³��������� �����-������� � ��������� ��������� ���� ListBox
            DisplayArray(array, listBox1);
            DisplayArray(array, listBox2);
            DisplayArray(array, listBox3);
        }

        // ���������� ���������� ������� �������� - �������� ����� ��������
        private void backgroundWorker2_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // ���� ���� ���������� ����������
            if (fCancelBub)
            {
                // ����������� �������� �������� ���������
                label5.Text = "";
                
                // ³��������� �����-�������
                DisplayArray(array, listBox1);
                fCancelBub = false;
            }
            else
            {
                // ����������� ��� �� ������� ����
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsBubble;
                label5.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // ³��������� ������������ �����
                DisplayArray(arrayBub, listBox1);
            }
            
            // ����������� ���� �������� ���������
            progressBar1.Value = 0;
            button1.Enabled = true;
        }

        // ���������� ������ ���������� ���������
        private void backgroundWorker3_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // ���� ���� ���������� ����������
            if (fCancelIns)
            {
                // ����������� �������� �������� ���������
                label6.Text = "";
                
                // ³��������� �����-�������
                DisplayArray(array, listBox2);
                fCancelIns = false;
            }
            else
            {
                // ����������� ��� �� ������� ����
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsIns;
                label6.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // ³��������� ������������ �����
                DisplayArray(arrayIns, listBox2);
            }
            // ����������� ���� �������� ���������
            progressBar2.Value = 0;
            button1.Enabled = true;
        }

        // ���������� ���������� �������
        private void backgroundWorker4_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            // ���� ���� ���������� ����������
            if (fCancelSel)
            {
                // ����������� �������� �������� ���������
                label7.Text = "";
                
                // ³��������� �����-�������
                DisplayArray(array, listBox3);
                fCancelSel = false;
            }
            else
            {
                // ����������� ��� �� ������� ����
                TimeSpan time = new TimeSpan(DateTime.Now.Ticks) - tsSel;
                label7.Text = String.Format("{0}.{1}.{2}.{3}", time.Hours, time.Minutes,
                time.Seconds, time.Milliseconds);
                
                // ³��������� ������������ �����
                DisplayArray(arraySel, listBox3);
            }
            // ����������� ���� �������� ���������
            progressBar3.Value = 0;
            button1.Enabled = true;
        }
    }
}
