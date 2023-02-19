using System;

enum MonthName
{
  January,
  February,
  March,
  April,
  May,
  June,
  July,
  August,
  September,
  October,
  November,
  December
}

public class Lab03
{
  public static void Main()
  {
    string line;
    int dayNum, yearNum;

    Console.WriteLine("Please enter a year number: ");
    line = Console.ReadLine();
    yearNum = int.Parse(line);

    bool isLeapYear = yearNum % 4 == 0;
    int maxDayNum = isLeapYear ? 366 : 365;

    try
    {
      Console.WriteLine("Please enter a day number between 1 and {0}: ", maxDayNum);
      line = Console.ReadLine();
      dayNum = int.Parse(line);

      if (dayNum < 1 || dayNum > maxDayNum)
      {
        throw new ArgumentOutOfRangeException("Day out of range");
      }
    }
    catch (System.Exception caught)
    {
      Console.WriteLine("Error {0}", caught.Message);
      throw;
    }

    int monthNum = 0;

    foreach (int daysInMonth in isLeapYear ? DaysInLeapMonths : DaysInMonths)
    {
      if (dayNum <= daysInMonth)
      {
        break;
      }
      else
      {
        dayNum -= daysInMonth;
        monthNum++;
      }
    }

    MonthName temp = (MonthName)monthNum;
    string monthName = temp.ToString();

    Console.WriteLine("{0},{1}", dayNum, monthName);
  }

  static System.Collections.ICollection DaysInMonths
      = new int[12] { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };

  static System.Collections.ICollection DaysInLeapMonths
  = new int[12] { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
}
