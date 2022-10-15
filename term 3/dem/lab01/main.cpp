// Variant 11

#include <iostream>
#include "transformations.hpp"

using namespace std;

int main()
{
  int i;
  int index;
  int amount;
  char conv_num;
  char num;
  char yes;
  long double ldnum;
  size_t binary_num;
  size_t reversed;

  cout << "Type 1 to transform char to binary" << endl;
  cout << "Type 2 to transform long double to binary" << endl;
  cout << "Type 0 to exit" << endl;

  while (i != 0)
  {
    cout << "Enter command: ";
    cin >> i;
    cout << endl;

    switch (i)
    {
    case 1:
      cout << "Enter your char: ";
      cin >> num;
      cout << endl;

      conv_num = (char)atoi(&num);
      binary_num = to_binary<char>(conv_num);

      cout << "Do you want to mirror some numbers? y/N" << endl;

      cin >> yes;

      if (yes == 'y')
      {
        cout << "Enter an index: ";
        cin >> index;

        cout << "Enter an amount of numbers to shuffle: ";
        cin >> amount;

        reversed = partial_inverse(conv_num, index, amount);
      }

      break;

    case 2:
      cout << "Enter your long double: ";
      cin >> ldnum;
      cout << endl;

      binary_num = to_binary<long double>(ldnum);

      cout << "Do you want to mirror some numbers? y/N" << endl;
      cin >> yes;

      if (yes == 'y')
      {
        cout << "Enter an index: ";
        cin >> index;

        cout << "Enter an amount of numbers to shuffle: ";
        cin >> amount;

        reversed = partial_inverse(binary_num, index, amount);
      }
      break;

    default:
      break;
    }
  }

  return 0;
}
