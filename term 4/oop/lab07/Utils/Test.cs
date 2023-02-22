namespace Utils
{
  using System;

  /// <summary>
  ///   This the test harness
  /// </summary>

  public class Test
  {
    public static void Main()
    {
      Console.WriteLine("Enter a message: ");
      string message = Console.ReadLine();

      Utils.Reverse(ref message);
      Console.WriteLine(message);
    }
  }
}
