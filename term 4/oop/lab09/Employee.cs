using System;
public class Employee : Person
{
  private string position { get; set; }

  public Employee(string name, string lastName_, Faculty faculty_, Department department_, string pos) :
  base(name, lastName_, faculty_, department_)
  {
    this.position = pos;
  }

}