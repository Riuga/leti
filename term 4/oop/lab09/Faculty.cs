using System;
public class Faculty
{
  public var departments = new List<Department>();
  private string name;
  public void Faculty(string name_)
  {
    this.name = name_;
  }

  public setDepartments()
  {
    int amount = Int.Parse(Console.ReadLine("Enter amount of departments: "));
    for (int i = 0; i < amount; i++)
    {
      string dep = Console.ReadLine("Enter department name: ");
      departments.Add(new Department(dep));
    }
  }
}