/*
  Lab01 by Moskvichev Sergei, group 1301
  Variant 7
  Проверка на содержание другого списка в списке, можно сделать целочисленного типа

  1. добавление в конец списка
  2. добавление в начало списка
  3. удаление последнего элемента
  4. удаление первого элемента
  5. добавление элемента по индексу (вставка перед элементом, который был ранее доступен по этому индексу)
  6. получение элемента по индексу
  7. удаление элемента по индексу
  8. получение размера списка
  9. удаление всех элементов списка
  10. замена элемента по индексу на передаваемый элемент
  11. проверка на пустоту списка
*/

#include <iostream>
#include "singly_linked_list.hpp"

using namespace std;

void show_menu()
{
  cout << "Type 1 to show menu" << endl;
  cout << "Type 2 to push an element back" << endl;
  cout << "Type 3 to push an element front" << endl;
  cout << "Type 4 to delete the last element" << endl;
  cout << "Type 5 to delete the first element" << endl;
  cout << "Type 6 to add an element by index" << endl;
  cout << "Type 7 to get an element by index" << endl;
  cout << "Type 8 to remove an element by index" << endl;
  cout << "Type 9 to get size of the list" << endl;
  cout << "Type 10 to clear the list" << endl;
  cout << "Type 11 to change an element" << endl;
  cout << "Type 12 to check the list on emptiness" << endl;
  cout << "Type 13 to print a list" << endl;
  cout << "Type 0 to exit" << endl;
}

int main()
{
  int i;
  int index;
  int val;
  List new_list;

  show_menu();
  while (i != 0)
  {
    cin >> i;

    switch (i)
    {
    case 1:
      show_menu();
      break;
    case 2:
      cout << "Enter a value: " << endl;
      cin >> val;
      new_list.push_back(val);
      break;
    case 3:
      cout << "Enter a value: " << endl;
      cin >> val;
      new_list.push_front(val);
      break;
    case 4:
      cout << "Element was removed" << endl;
      new_list.pop_back();
      break;
    case 5:
      cout << "Element was removed" << endl;
      new_list.pop_front();
      break;
    case 6:
      cout << "Enter a value: " << endl;
      cin >> val;
      cout << "Enter an index: " << endl;
      cin >> index;
      new_list.insert_by_index(index, val);
      break;
    case 7:
      cout << "Enter an index: " << endl;
      cin >> index;
      cout << "An element: " << new_list.get_value(index) << endl;
      break;
    case 8:
      cout << "Enter an index: " << endl;
      cin >> index;
      new_list.remove_element(index);
      break;
    case 9:
      cout << "Size: " << new_list.get_size() << endl;
      break;
    case 10:
      new_list.clear();
      cout << "List was cleared" << endl;
      break;
    case 11:
      cout << "Enter a value: " << endl;
      cin >> val;
      cout << "Enter an index: " << endl;
      cin >> index;
      new_list.change_value(index, val);
      break;
    case 12:
      if (new_list.is_empty())
      {
        cout << "List is empty" << endl;
      }
      else
      {
        cout << "List is not empty" << endl;
      }
      break;

    case 13:
      new_list.print_list();
      break;

    default:
      break;
    }
  }

  return 0;
}