#include "conio.h"
#include "dos.h"

int x1 = 20;
int y1 = 10;
int x2 = 60;
int y2 = 20;
int T = 1500;
int num_colors = 16;

enum
{
	ENTIRE,
	UP,
	DOWN
};

void scroll(int direction, int lines, char l_row, char l_col, char r_row, char r_col, char attr)
{
	union REGS r;
	if (direction == DOWN)
	{
		r.h.ah = 7;
	}
	else
	{
		r.h.ah = 6;
	}
	r.h.al = lines;
	r.h.ch = l_row;
	r.h.cl = l_col;
	r.h.dh = r_row;
	r.h.dl = r_col;
	r.h.bh = attr;
	int86(0x10, &r, &r);
}

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
			textcolor(j);

			Background(i);
			Text(j);
			cprintf("\r\n");

			scroll(UP, 2, y1 - 1, x1 - 1, y2 - 1, x2 - 1, (i * 16 | j));
			delay(T);
		}
	}
	getch();
	return 0;
}
