namespace Utils
{
  using System;

  class Utils
  {
    public static void Display(object item)
    {
      IPrintable ip = item as IPrintable;

      if (ip != null)
      {
        ip.Print();
      }
      else
      {
        Console.WriteLine(item.ToString());
      }
    }
  }
}
