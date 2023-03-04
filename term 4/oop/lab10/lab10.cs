using System;
using System.IO;

namespace OopLabs.Delegates
{
  class Lab10
  {
    // private delegate void Log(string message);

    static void DoSomething(Action<string> log)
    {
      log(DateTime.Now + " log message");
    }

    static void LogToFile(string message)
    {
      string myDocsPath =
      Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
      string logFilePath = Path.Combine(myDocsPath, "log.txt");
      File.AppendAllText(logFilePath, message + Environment.NewLine);
    }

    static void Main()
    {
      DoSomething(LogToFile);
      DoSomething(delegate (string message) { Console.WriteLine(message); });
      DoSomething(message => Console.WriteLine(message));
      DoSomething(Console.WriteLine);
      Console.ReadKey();
    }
  }
}
