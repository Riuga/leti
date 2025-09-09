using System;
public class University
{
  private string name { get; }
  private int foundation_year { get; }
  private Employee rector { get; set; }
  private var employees = new List<Employee>() { rector };
  private var students = new List<Student>();
  public var faculties = new List<Faculty>();


  public void University(string name_, int foundation_year_, Employee rector_)
  {
    this.name = name_;
    this.foundation_year = foundation_year_;
    this.rector = rector_;
  }

  public void HireEmployee()
  {
    Console.WriteLine("Type employee data: ");
    string name = Console.ReadLine("First name: ");
    string lastName = Console.ReadLine("Last name: ");
    Department department = Console.ReadLine("Name: "); // rewrite
    string pos = Console.ReadLine("Position: ");
    var employee = new Employee(name, lastName, department, pos);
    employees.Add(employee);
  }

  public void FireEmployee()
  {

  }

  public void EnrollStudent(Student student)
  {
    Console.WriteLine("Type employee data: ");
    string name = Console.ReadLine("First name: ");
    string lastName = Console.ReadLine("Last name: ");
    Department department = Console.ReadLine("Name: "); // rewrite
    string degree = Console.ReadLine("Degree: ");
    int grade = int.Parse(Console.ReadLine("Grade: "));
    var student = new Student(name, lastName, department, degree, grade);
    students.Add(student);
  }

  public void ExpelStudent()
  {

  }
}
