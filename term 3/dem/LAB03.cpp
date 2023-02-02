#include "stdio.h";
#include "math.h";
#include "dos.h";
#include "graphics.h";
#include "string.h";
#include "conio.h";

int x_max, y_max;
const float pi = 3.14;
float begin = pi / 2.0;
float end = 7.0 * pi;
float step;
int num_point;
int x1, x2, y1, y2;
float x, y;
float max_value = 0;

int main()
{
	clrscr();

	int graph_driver;
	int graph_mode;
	graph_driver = DETECT;
	graph_mode = 0;
	initgraph(&graph_driver, &graph_mode, "C:\\TurboC3\\BGI");

	x_max = getmaxx();
	y_max = getmaxy();
	x1 = 30;
	x2 = x_max - x1;
	y2 = 30;
	y1 = y_max - y2;
	num_point = x2 - x1;

	x1 = 40;
	y1 = y_max - 30;
	x2 = x_max - 30;
	y2 = 30;
	num_point = x2 - x1;
	setlinestyle(0, 1, 3);
	setcolor(BLUE);
	rectangle(2, 0, x_max - 2, y_max - 15);
	setfillstyle(SOLID_FILL, BLACK);
	floodfill(20, 20, BLUE);

	setlinestyle(0, 1, 1);
	line(x1 + 20, y1 - 5, x1 + 20, y2 - 20);
	line(x1 - 2, y1 - 220, x2 + 15, y1 - 220);
	outtextxy(x1 + 40, y2 + 40, "sin^2(x)-cos^2(x)");
	outtextxy(x2 + 3, y1 - 219, "x");
	int i;
	for (i = 1; i < 23; ++i)
		line(x1 + 20, y1 - i * 20, x1 + 25, y1 - i * 20);
	for (i = 0; i < 29; ++i)
		line(x1 + 20 * i, y1 - 220, x1 + 20 * i, y1 - 225);
	outtextxy(x1 + 23, y1 - 218, "1.5");
	outtextxy(x1 + 20 * 5, y1 - 218, "3.5");
	outtextxy(x1 + 20 * 9, y1 - 218, "5.5");
	outtextxy(x1 + 20 * 13, y1 - 218, "7.5");
	outtextxy(x1 + 20 * 17, y1 - 218, "9.5");
	outtextxy(x1 + 20 * 21, y1 - 218, "11.5");
	outtextxy(x1 + 20 * 25, y1 - 218, "13.5");

	step = (float)(((end - begin) / 2.0) / num_point);
	x = begin;
	for (i = 0; i < num_point; i++)
	{
		y = (float)(pow(sin(x), 2.0) - pow(cos(x), 2.0));
		if (y > max_value)
			max_value = y;
		x += step;
	}
	x = begin;
	for (int j = 0; j < num_point; j++)
	{
		y = (float)(pow(sin(x), 2.0) - pow(cos(x), 2.0));
		putpixel(j + x1, (y1 - (int)(y / max_value * (float)(y1 - y2))) / 2 - 5, WHITE);
		x += step;
	}

	char cmax_value[10];
	sprintf(cmax_value, "%f", max_value);
	char str[24];
	strcpy(str, "MAX(f(x)) = ");
	strcat(str, cmax_value);
	setcolor(BLACK);
	rectangle(x1 + 25, y1 - 5, x1 + 200, y1 + 10);
	setfillstyle(SOLID_FILL, LIGHTCYAN);
	floodfill(x1 + 30, y1, BLACK);
	setcolor(WHITE);
	outtextxy(x1 + 30, y1, str);

	getch();
	closegraph();
	return 0;
}
