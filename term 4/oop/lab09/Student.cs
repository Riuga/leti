using System;
public class Student : Person
{
  private string degree { get; set; }
  private int grade { get; set; }

  public Student(string name, string lastName_, Faculty faculty_, Department department_, string degree_, int grade_) : base(name, lastName_, faculty_, department_)
  {
    this.degree = degree_;
    this.grade = grade_;
  }
}