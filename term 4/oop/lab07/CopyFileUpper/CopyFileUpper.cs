using System;
using System.IO;

public class CopyFileUpper
{
  public static void Main()
  {
    string sFrom, sTo;
    string sBuffer = "";

    StreamReader srFrom;
    StreamWriter swTo;

    Console.WriteLine("Enter file name to read: ");
    sFrom = Console.ReadLine();

    Console.WriteLine("Enter file name to write: ");
    sTo = Console.ReadLine();

    try
    {
      srFrom = new StreamReader(sFrom);
      swTo = new StreamWriter(sTo);

      while (srFrom.Peek() != -1)
      {
        sBuffer = srFrom.ReadLine();
        sBuffer = sBuffer.ToUpper();
        swTo.WriteLine(sBuffer);
      }

      srFrom.Close();
      swTo.Close();
    }
    catch (FileNotFoundException e)
    {
      Console.WriteLine("File not found: {0}", e.Source);
    }
    catch (System.Exception e)
    {
      Console.WriteLine(e.Source);
      throw;
    }
  }
}
