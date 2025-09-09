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

  public static void Factorial(int n, out int answer) {
    answer = 1;

    for (int i = n; i > 1; i--) {
      answer *= i;
    }
  }

  public static int RecursiveFactorial(int n) {
    return n == 1 ? n : n * RecursiveFactorial(n-1);
  }
}
