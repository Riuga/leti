using System;
using System.IO;

public class BankTransaction
{
  private readonly decimal amount;
  private readonly DateTime when;

  public BankTransaction(decimal tranAmount)
  {
    amount = tranAmount;
    when = DateTime.Now;
  }

  ~BankTransaction()
  {
    StreamWriter swFile = File.AppendText("Transactions.Dat");
    swFile.WriteLine("Date/Time: {0}\tAmount: {1}", when, amount);
    swFile.Close();
    GC.SuppressFinalize(this);
  }

  public decimal Amount()
  {
    return amount;
  }

  public DateTime When()
  {
    return when;
  }
}
