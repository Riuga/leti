// Variant 11

#include <iostream>
#include "transformations.hpp"

using namespace std;

int main()
{
  int i;
  char conv_num;
  char *num;
  long double ldnum;

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
      conv_num = (char)atoi(num);
      cout << to_binary<char>(conv_num) << endl;
      break;

    case 2:
      cout << "Enter your long double: ";
      cin >> ldnum;
      cout << endl;
      cout << to_binary<long double>(ldnum) << endl;
      break;

    default:
      break;
    }
  }

  return 0;
}
