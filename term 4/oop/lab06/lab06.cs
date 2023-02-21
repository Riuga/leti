using System;

public class Lab06
{
  public static void Main(string[] args)
  {
    BankAccount berts = CreateAccount.NewBankAccount();
    CreateAccount.Write(berts);

    BankAccount freds = CreateAccount.NewBankAccount();
    CreateAccount.Write(freds);

    CreateAccount.TestDeposit(berts);
    CreateAccount.TestDeposit(freds);

    CreateAccount.TestWithdraw(berts);
    CreateAccount.TestWithdraw(freds);
  }
}
