using System;

public enum AccountType
{
  Checking,
  Deposit,
}

public struct BankAccount
{
  public long accNo;
  public decimal accBal;
  public AccountType accType;

  public BankAccount(long no, decimal bal, AccountType type)
  {
    this.accNo = no;
    this.accBal = bal;
    this.accType = type;
  }
}
public class Lab02
{
  public static void Main(string[] args)
  {
    BankAccount goldAccount = new BankAccount(1, 30, AccountType.Checking);
    BankAccount platinumAccount = new BankAccount(2, 40, AccountType.Deposit);

    Console.WriteLine("Gold account: {0}, {1}, {2}", goldAccount.accNo, goldAccount.accBal, goldAccount.accType);
    Console.WriteLine("Platinum account: {0}, {1}, {2}", platinumAccount.accNo, platinumAccount.accBal, platinumAccount.accType);
  }
}
