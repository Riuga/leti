#include "dos.h"
#include "conio.h"
#include "stdio.h"
#include "iostream.h"
#include "string.h"

int ch = 0;
int left = 0;
int i = 0;

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
	textbackground(1);
	textcolor(16);
	clrscr();

	char str[50] = "Lorem ipsum dolor sit amet.";

	do
	{

		if (str[i] == ' ')
		{
			do
			{
				if (keypressed())
				{
					ch = code();
				}
			} while (ch != 32);
			cout << str[i];
			ch = 0;
			i++;
		}
		else
		{
			cout << str[i];
			i++;
		}
	} while (i < sizeof(str));

	getch();
	return 0;
}

