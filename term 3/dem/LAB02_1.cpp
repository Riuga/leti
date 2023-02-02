#include "conio.h"
#include "dos.h"

int x1 = 20;
int y1 = 10;
int x2 = 60;
int y2 = 20;
int T = 1500;
int num_colors = 16;

void Background(int background)
{
	cprintf("\r\n%d", ++background);
}

void Text(int text)
{
	cprintf("\r\n%d", ++text);
}

int main()
{
	window(x1, y1, x2, y2);
	textattr(112);
	for (int i = 0; i < num_colors; i++)
	{
		textbackground(i);
		for (int j = 0; j < num_colors; j++)
		{
			textcolor(j);û

			Background(i);
			Text(j);
			cprintf("\r\n");
			delay(T);
		}
	}
	getch();
	return 0;
}
