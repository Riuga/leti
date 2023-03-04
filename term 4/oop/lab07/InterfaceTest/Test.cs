namespace Utils
{
  using System;

  public class Test
  {
    public static void Main()
    {
      int i = 0;
      ulong ul = 0;
      string s = "Test";

      Console.WriteLine(Utils.isFormattable(i));
      Console.WriteLine(Utils.isFormattable(ul));
      Console.WriteLine(Utils.isFormattable(s));
    }
  }
}
