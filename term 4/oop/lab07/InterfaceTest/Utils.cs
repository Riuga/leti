namespace Utils
{
  using System;

  class Utils
  {
    public static bool isFormattable(object x)
    {
      return x is IFormattable;
    }
  }
}
