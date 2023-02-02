#include "dos.h"
#include "conio.h"
#include "stdio.h"

int X1 = 20;
int Y1 = 10;
int X2 = 60;
int Y2 = 20;
int x = 1;
int y = 1;
int ch = 0;
int left = 0;

int keypressed()
{
	union REGS r;
	r.h.ah = 0x0B;
	int86(0x21, &r, &r);

	return r.h.al;
}

int code()
{
	union REGS r;
	r.h.ah = 0x7;
	int86(0x21, &r, &r);
	return r.h.al;
}
	

int main()
{
	window(X1, Y1, X2, Y2);
	textbackground(10);
	textcolor(5);

	clrscr();
	do {
		do

		{
			clrscr();

			if ((left == 1) && ((x - 1) >= 0))
				x -= 1;

			if ((left == 0) && ((x + 1) <= (X2 - X1)))
				x += 1;

			gotoxy(x, y);
			putch('*');
			delay(100);

		} while (keypressed() == 0);

		ch = code();

		if (ch == 0 || ch == 224)
		{
			switch (code())
			{
			case 61:
				left = 1;
				break;

			case 62:
				left = 0;
				break;
			}
		}

	} while (ch != 27);
	return 0;
}

