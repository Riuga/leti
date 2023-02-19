using System;

public class Utils
{
  public static int Greater(int a, int b)
  {
    return a > b ? a : b;
  }

  public static void Swap(ref int a, ref int b) {
    int temp = a;
    a = b;
    b = temp;
  }

  public static int Factorial(int n) {
    int result = 1;

    for (int i = n; i > 1; i--) {
      result *= i;
    }

    return result;
  }

  public static int RecursiveFactorial(int n) {
    return n == 1 ? n : n * RecursiveFactorial(n-1);
  }
}
