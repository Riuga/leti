using System;

class CreateAccount
{
  public static BankAccount NewBankAccount()
  {
    BankAccount created = new BankAccount();

    // Console.Write("Enter the account number   : ");
    // long number = long.Parse(Console.ReadLine());

    // long number = BankAccount.NextNumber();

    Console.Write("Enter the account balance  : ");
    decimal balance = decimal.Parse(Console.ReadLine());

    created.Populate(balance);

    return created;
  }

  public static void Write(BankAccount toWrite)
  {
    Console.WriteLine("Account number is {0}", toWrite.getNumber());
    Console.WriteLine("Account balance is {0}", toWrite.getBalance());
    Console.WriteLine("Account type is {0}", toWrite.getAccType());
  }

  public static void TestDeposit(BankAccount acc)
  {
    Console.WriteLine("Enter amount to deposit: ");
    decimal amount = decimal.Parse(Console.ReadLine());
    acc.Deposit(amount);
    Write(acc);
  }

  public static void TestWithdraw(BankAccount acc)
  {
    Console.WriteLine("Enter amount to withdraw: ");
    decimal amount = decimal.Parse(Console.ReadLine());
    bool isEnough = acc.Withdraw(amount);
    Console.WriteLine(isEnough ? "Withdrawed succesfully" : "Not enough money");
    Write(acc);
  }
}
