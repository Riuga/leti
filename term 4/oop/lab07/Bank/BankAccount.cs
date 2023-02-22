using System;

class BankAccount
{
  private long accNo;
  private decimal accBal;
  private AccountType accType;

  private static long nextNumber = 123;

  public void Populate(decimal balance)
  {
    accNo = NextNumber();
    accBal = balance;
    accType = AccountType.Checking;
  }

  public bool Withdraw(decimal amount)
  {
    bool sufficientFunds = accBal >= amount;
    if (sufficientFunds)
    {
      accBal -= amount;
    }
    return sufficientFunds;
  }

  public decimal Deposit(decimal amount)
  {
    accBal += amount;
    return accBal;
  }

  public long Number()
  {
    return accNo;
  }

  public decimal Balance()
  {
    return accBal;
  }

  public AccountType Type()
  {
    return accType;
  }

  private static long NextNumber()
  {
    return nextNumber++;
  }

  public void TransferFrom(BankAccount accForm, decimal amount)
  {
    bool isWithdrawed = accForm.Withdraw(amount);
    if (isWithdrawed)
    {
      Deposit(amount);
    }
  }

  public void Write()
  {
    Console.WriteLine("Number: {0}", Number());
    Console.WriteLine("Balance: {0}", Balance());
    Console.WriteLine("Type: {0}", Type());
  }
}
