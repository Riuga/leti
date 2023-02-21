public class BankAccount
{
  private long accNo;
  private decimal accBal;
  private AccountType accType;
  private static long nextAccNo = 123;

  private static long NextNumber()
  {
    return ++nextAccNo;
  }

  public void Populate(decimal balance)
  {
    accNo = NextNumber();
    accBal = balance;
    accType = AccountType.Checking;
  }

  public long getNumber()
  {
    return accNo;
  }

  public decimal getBalance()
  {
    return accBal;
  }

  public AccountType getAccType()
  {
    return accType;
  }

  public decimal Deposit(decimal amount)
  {
    accBal += amount;
    return accBal;
  }

  public bool Withdraw(decimal amount)
  {
    bool isEnough = amount <= accBal;
    if (isEnough)
    {
      accBal -= amount;
    }
    return isEnough;
  }
}
