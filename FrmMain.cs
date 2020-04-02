using System;
using System.Windows.Forms;

namespace Longhorn_TN3270
{
    public partial class FrmMain : Form
    {
        private readonly Keygen _keygen = new Keygen();

        public FrmMain()
        {
            InitializeComponent();
        }

        private void tbxRegCode_MouseClick(object sender, MouseEventArgs e)
        {
            tbxRegCode.SelectAll();
        }

        private void btnSubmit_Click(object sender, EventArgs e)
        {
            tbxRegCode.Text = _keygen.Generate(tbxUserName.Text);
        }
    }
}
