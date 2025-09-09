using System;

public class Test
{
  public static void Main()
  {
    BankAccount b1 = new BankAccount();
    BankAccount b2 = new BankAccount();

    b1.Populate(100);
    b1.Write();

    b2.Populate(100);
    b2.Write();

    int n = Int16.Parse(Console.ReadLine());

    b1.TransferFrom(b2, n);
    b1.Write();
    b2.Write();
  }
}
