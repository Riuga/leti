using System;

public class Lab01
{
  static public void Main(string[] args)
  {
    string myName, temp;
    int i, j, k;

    Console.WriteLine("Please enter your name");
    myName = Console.ReadLine();
    Console.WriteLine("Hello {0}", myName);
    Console.WriteLine("Enter an integer: ");
    temp = Console.ReadLine();
    i = Int32.Parse(temp);
    Console.WriteLine("Enter another integer: ");
    temp = Console.ReadLine();
    j = Int32.Parse(temp);

    try
    {
      k = i / j;
      Console.WriteLine("{0} / {1} = {2}", i, j, k);
    }
    catch (System.Exception)
    {
      Console.WriteLine("Incorrect data");
      throw;
    }
  }
}