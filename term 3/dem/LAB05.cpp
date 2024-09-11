#include <dos.h>
#include <conio.h>
#include <iostream.h>

void interrupt (*oldfunc)(...);

int is_dot_pressed = 0;
char str[100];
int left = 0;
int length = 0;

void get_key()
{
	union REGS r;
	r.h.ah = 0x6;
	r.h.dl = 0xff;
	int86(0x21, &r, &r);
}

void interrupt my_interrupt(...)
{
	if (is_dot_pressed == 0)
	{
		get_key();
		if (_AL != '.')
		{
			if (_AL == ' ')
			{
				str[length] = _AL;
				length++;

				while (left < length)
				{
					cout << str[left];
					left++;
				}
			}
			else if (_AL != NULL)
			{
				str[length] = _AL;
				length++;
			}
		}
		else
		{
			while (left < length)
			{
				cout << str[left];
				left++;
			}
			cout << ".\n";
			is_dot_pressed = 1;
		}
	}

	_chain_intr(oldfunc);
}

int main()
{
	textbackground(1);
	textcolor(16);
	clrscr();

	int counter = 0;
	oldfunc = _dos_getvect(0x9);
	_dos_setvect(0x9, my_interrupt);
	while (is_dot_pressed == 0)
	{
		if (counter == 0)
		{
			cout << "Enter a sentence. Text will be displayed when you press space, program will end when you press dot\n";
			counter++;
		}
	}
	_dos_setvect(0x9, oldfunc);
	getch();
	return 0;
}