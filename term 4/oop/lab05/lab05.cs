using System;
using System.IO;

public class Lab05
{
  public static void Summarize(char[] arr)
  {
    int vowels = 0, consonants = 0, newLine = 0;

    foreach (var ch in arr)
    {
      if ("AEIOUaeiou".IndexOf(ch) != -1)
      {
        vowels += 1;
      }
      else if (ch == '\n')
      {
        newLine += 1;
      }
      else
      {
        consonants += 1;
      }
    }

    Console.WriteLine("Vowels: {0}; Consonants: {1}; New line symbols: {2}", vowels, consonants, newLine);
  }

  public static void WriteMatrix(int[,] matrix)
  {
    for (int i = 0; i < 2; i++)
    {
      for (int j = 0; j < 2; j++)
      {
        Console.Write(matrix[i, j] + " ");
      }
      Console.WriteLine();
    }
  }

  public static int[,] NewMatrix()
  {
    int[,] matrix = new int[2, 2];

    for (int n = 0; n < 2; n++)
    {
      for (int m = 0; m < 2; m++)
      {
        Console.WriteLine("Enter number: ");
        matrix[n, m] = Convert.ToInt32(Console.ReadLine());
      }
      Console.WriteLine();
    }

    WriteMatrix(matrix);

    return matrix;
  }

  public static int[,] MatrixMultiply(int[,] m1, int[,] m2)
  {
    var m1Rows = m1.GetLength(0);
    var m1Cols = m1.GetLength(1);
    var m2Rows = m2.GetLength(0);
    var m2Cols = m2.GetLength(1);

    if (m1Cols != m2Rows)
      throw new InvalidOperationException
        ("Columns of first matrix must equal to rows of second matrix");

    int[,] result = new int[m1Rows, m2Cols];

    for (int m1_row = 0; m1_row < m1Rows; m1_row++)
    {
      for (int m2_col = 0; m2_col < m2Cols; m2_col++)
      {
        for (int m1_col = 0; m1_col < m1Cols; m1_col++)
        {
          result[m1_row, m2_col] +=
            m1[m1_row, m1_col] *
            m2[m1_col, m2_col];
        }
      }
    }

    return result;
  }

  public static void Main(string[] args)
  {

    Console.WriteLine("Args length: {0}", args.Length);

    string fileName = args[0];

    FileStream stream = new FileStream(fileName, FileMode.Open);
    StreamReader reader = new StreamReader(stream);

    foreach (var arg in args)
    {
      Console.WriteLine("Arg: {0}", arg);
    }

    long fileLength = stream.Length;
    Console.WriteLine("File length: {0}", fileLength);

    char[] context = new char[fileLength];

    for (int i = 0; i < fileLength; i++)
    {
      context[i] = (char)reader.Read();
    }

    Console.WriteLine("Text:");
    Console.WriteLine(context);
    reader.Close();

    Summarize(context);

    int[,] m1 = NewMatrix();
    int[,] m2 = NewMatrix();
    int[,] multiplyed = MatrixMultiply(m1, m2);
    Console.WriteLine("Multiplyed matrix:");
    WriteMatrix(multiplyed);
  }
}
