/*
  TODO:
  16. Проверка на содержание другого списка в списке, можно сделать целочисленного типа
*/
#include <iostream>

using namespace std;

struct Node
{
  int value;
  Node *next_element;

  Node(int val) : value(val), next_element(nullptr){};
};

struct List
{
  Node *first_element;
  Node *last_element;

  List() : first_element(nullptr), last_element(nullptr){};

  bool is_empty()
  {
    return first_element == nullptr;
  }

  void push_front(int val)
  {
    Node *new_element = new Node(val);
    if (is_empty())
    {
      first_element = new_element;
      last_element = new_element;

      return;
    }

    new_element->next_element = first_element;
    first_element = new_element;
  }

  void push_back(int val)
  {
    Node *new_element = new Node(val);

    if (is_empty())
    {
      first_element = new_element;
      last_element = new_element;

      return;
    }
    last_element->next_element = new_element;
    last_element = new_element;
  }

  void pop_front()
  {
    if (is_empty())
    {
      return;
    }
    Node *temp = first_element;
    first_element = temp->next_element;
    delete temp;
  }

  void pop_back()
  {
    if (is_empty())
    {
      return;
    }
    if (first_element == last_element)
    {
      pop_front();
    }
    Node *temp = first_element;
    while (temp->next_element != last_element)
    {
      temp = temp->next_element;
    }
    temp->next_element = nullptr;
    delete last_element;
    last_element = temp;
  }

  unsigned int get_size()
  {
    unsigned int size = 0;
    Node *temp = first_element;
    while (temp)
    {
      temp = temp->next_element;
      size++;
    }
    return size;
  }

  Node *get_element(unsigned int index)
  {
    if (is_empty() || index >= get_size())
    {
      return nullptr;
    }

    Node *element = first_element;
    unsigned int i = 0;
    while (i < index)
    {
      element = element->next_element;
      i++;
    }

    return element;
  }

  int get_value(unsigned int index)
  {
    return get_element(index)->value;
  }

  void remove_element(unsigned int index)
  {
    if (is_empty() || index >= get_size())
    {
      return;
    }
    Node *del_element = get_element(index);
    Node *temp = first_element;
    unsigned int i = 0;
    while (i < index - 1)
    {
      temp = temp->next_element;
      i++;
    }

    temp->next_element = del_element->next_element;
    delete del_element;
  }

  void clear()
  {
    while (!is_empty())
    {
      pop_front();
    }
  }

  void change_value(unsigned int index, int val)
  {
    Node *change = get_element(index);
    change->value = val;
  }

  void insert_by_index(unsigned int index, int val)
  {
    Node *new_element = new Node(val);
    new_element->next_element = get_element(index);
    get_element(index - 1)->next_element = new_element;
  }

  void print_list()
  {
    if (is_empty())
    {
      return;
    }
    Node *temp = first_element;
    while (temp)
    {
      cout << temp->value << " ";
      temp = temp->next_element;
    }
    cout << endl;
  }
};
