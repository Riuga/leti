using System;

public class Lab04
{
  public static void Main(string[] args)
  {
    Console.WriteLine("Enter first num:");
    int x = int.Parse(Console.ReadLine());

    Console.WriteLine("Enter second num:");
    int y = int.Parse(Console.ReadLine());

    Console.WriteLine("Your nums: {0}, {1}", x, y);
    Utils.Swap(ref x, ref y);
    Console.WriteLine("Swapped nums: {0}, {1}", x, y);

    int greater = Utils.Greater(x, y);
    Console.WriteLine("The greatest value is {0}", greater);

    Console.WriteLine("Enter a num for factorial:");
    int z = int.Parse(Console.ReadLine());

    int factorial = Utils.Factorial(z);
    Console.WriteLine("Factorial of {0} is {1}", z, factorial);
    
    int recursive = Utils.RecursiveFactorial(z);
    Console.WriteLine("Factorial of {0} is {1} (calculated recursively)", z, recursive);

  }
}
