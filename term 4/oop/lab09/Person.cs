using System;
public class Person
{
  private string firsName { get; }
  private string lastName { get; }
  private Faculty faculty { get; }
  private Department department { get; }

  public Person(string name, string lastName_, Faculty faculty_, Department department_)
  {
    this.firsName = name;
    this.lastName = lastName_;
    this.faculty = faculty_;
    this.department = department_;
  }

}