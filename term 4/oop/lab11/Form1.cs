namespace OopLabs.Linq
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            listBox1.DataSource = Album.GetAlbums().Select(album => album.Artist).Distinct().ToList();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            listBox2.DataSource = Album.GetAlbums().Where(album => album.Artist == listBox1.SelectedItem.ToString()).OrderByDescending(album => album.Date).ToList();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void listBox2_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}