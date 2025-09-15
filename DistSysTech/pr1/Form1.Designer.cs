namespace pr1
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            label5 = new Label();
            label6 = new Label();
            label7 = new Label();
            button1 = new Button();
            button2 = new Button();
            button3 = new Button();
            listBox2 = new ListBox();
            listBox3 = new ListBox();
            progressBar1 = new ProgressBar();
            progressBar2 = new ProgressBar();
            progressBar3 = new ProgressBar();
            textBox1 = new TextBox();
            backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            backgroundWorker2 = new System.ComponentModel.BackgroundWorker();
            backgroundWorker3 = new System.ComponentModel.BackgroundWorker();
            backgroundWorker4 = new System.ComponentModel.BackgroundWorker();
            listBox1 = new ListBox();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(12, 9);
            label1.Name = "label1";
            label1.Size = new Size(60, 15);
            label1.TabIndex = 0;
            label1.Text = "Array size:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(12, 174);
            label2.Name = "label2";
            label2.Size = new Size(84, 15);
            label2.TabIndex = 1;
            label2.Text = "Bubble sorting";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(160, 174);
            label3.Name = "label3";
            label3.Size = new Size(93, 15);
            label3.TabIndex = 2;
            label3.Text = "Insertion sorting";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(310, 174);
            label4.Name = "label4";
            label4.Size = new Size(95, 15);
            label4.TabIndex = 3;
            label4.Text = "Selection sorting";
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Location = new Point(12, 426);
            label5.Name = "label5";
            label5.Size = new Size(0, 15);
            label5.TabIndex = 4;
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Location = new Point(160, 426);
            label6.Name = "label6";
            label6.Size = new Size(0, 15);
            label6.TabIndex = 5;
            // 
            // label7
            // 
            label7.AutoSize = true;
            label7.Location = new Point(310, 426);
            label7.Name = "label7";
            label7.Size = new Size(0, 15);
            label7.TabIndex = 6;
            // 
            // button1
            // 
            button1.Location = new Point(273, 9);
            button1.Name = "button1";
            button1.Size = new Size(147, 23);
            button1.TabIndex = 7;
            button1.Text = "Generate array";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(12, 93);
            button2.Name = "button2";
            button2.Size = new Size(75, 23);
            button2.TabIndex = 8;
            button2.Text = "Sort";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // button3
            // 
            button3.Location = new Point(123, 93);
            button3.Name = "button3";
            button3.Size = new Size(75, 23);
            button3.TabIndex = 9;
            button3.Text = "Stop";
            button3.UseVisualStyleBackColor = true;
            button3.Click += button3_Click;
            // 
            // listBox2
            // 
            listBox2.FormattingEnabled = true;
            listBox2.ItemHeight = 15;
            listBox2.Location = new Point(162, 192);
            listBox2.Name = "listBox2";
            listBox2.Size = new Size(120, 199);
            listBox2.TabIndex = 11;
            // 
            // listBox3
            // 
            listBox3.FormattingEnabled = true;
            listBox3.ItemHeight = 15;
            listBox3.Location = new Point(310, 192);
            listBox3.Name = "listBox3";
            listBox3.Size = new Size(120, 199);
            listBox3.TabIndex = 12;
            // 
            // progressBar1
            // 
            progressBar1.Location = new Point(12, 397);
            progressBar1.Name = "progressBar1";
            progressBar1.Size = new Size(121, 23);
            progressBar1.TabIndex = 15;
            // 
            // progressBar2
            // 
            progressBar2.Location = new Point(160, 397);
            progressBar2.Name = "progressBar2";
            progressBar2.Size = new Size(121, 23);
            progressBar2.TabIndex = 16;
            // 
            // progressBar3
            // 
            progressBar3.Location = new Point(310, 397);
            progressBar3.Name = "progressBar3";
            progressBar3.Size = new Size(121, 23);
            progressBar3.TabIndex = 17;
            // 
            // textBox1
            // 
            textBox1.Location = new Point(81, 10);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(169, 23);
            textBox1.TabIndex = 18;
            // 
            // backgroundWorker1
            // 
            backgroundWorker1.WorkerReportsProgress = true;
            backgroundWorker1.WorkerSupportsCancellation = true;
            backgroundWorker1.DoWork += backgroundWorker1_DoWork;
            backgroundWorker1.ProgressChanged += backgroundWorker1_ProgressChanged;
            backgroundWorker1.RunWorkerCompleted += backgroundWorker1_RunWorkerCompleted;
            // 
            // backgroundWorker2
            // 
            backgroundWorker2.WorkerReportsProgress = true;
            backgroundWorker2.WorkerSupportsCancellation = true;
            backgroundWorker2.DoWork += backgroundWorker2_DoWork;
            backgroundWorker2.ProgressChanged += backgroundWorker2_ProgressChanged;
            backgroundWorker2.RunWorkerCompleted += backgroundWorker2_RunWorkerCompleted;
            // 
            // backgroundWorker3
            // 
            backgroundWorker3.WorkerReportsProgress = true;
            backgroundWorker3.WorkerSupportsCancellation = true;
            backgroundWorker3.DoWork += backgroundWorker3_DoWork;
            backgroundWorker3.ProgressChanged += backgroundWorker3_ProgressChanged;
            backgroundWorker3.RunWorkerCompleted += backgroundWorker3_RunWorkerCompleted;
            // 
            // backgroundWorker4
            // 
            backgroundWorker4.WorkerReportsProgress = true;
            backgroundWorker4.WorkerSupportsCancellation = true;
            backgroundWorker4.DoWork += backgroundWorker4_DoWork;
            backgroundWorker4.ProgressChanged += backgroundWorker4_ProgressChanged;
            backgroundWorker4.RunWorkerCompleted += backgroundWorker4_RunWorkerCompleted;
            // 
            // listBox1
            // 
            listBox1.FormattingEnabled = true;
            listBox1.ItemHeight = 15;
            listBox1.Location = new Point(12, 192);
            listBox1.Name = "listBox1";
            listBox1.Size = new Size(120, 199);
            listBox1.TabIndex = 19;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(445, 450);
            Controls.Add(listBox1);
            Controls.Add(textBox1);
            Controls.Add(progressBar3);
            Controls.Add(progressBar2);
            Controls.Add(progressBar1);
            Controls.Add(listBox3);
            Controls.Add(listBox2);
            Controls.Add(button3);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(label7);
            Controls.Add(label6);
            Controls.Add(label5);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Name = "Form1";
            Text = "Demo of BackgroundWorker class";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private Label label5;
        private Label label6;
        private Label label7;
        private Button button1;
        private Button button2;
        private Button button3;
        private ListBox listBox1;
        private ListBox listBox2;
        private ListBox listBox3;
        private ProgressBar progressBar1;
        private ProgressBar progressBar2;
        private ProgressBar progressBar3;
        private TextBox textBox1;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private System.ComponentModel.BackgroundWorker backgroundWorker2;
        private System.ComponentModel.BackgroundWorker backgroundWorker3;
        private System.ComponentModel.BackgroundWorker backgroundWorker4;
    }
}
