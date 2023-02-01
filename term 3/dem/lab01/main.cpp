#include <iostream>
#include <cmath>
#include <cstdint>
#include <string>

using namespace std;

const uint8_t BYTE_SIZE = 8;

union type
{
  unsigned long long ll;
  long double d;
};

template <typename T>
void to_binary(const T &num)
{
  const size_t bits = BYTE_SIZE * sizeof(num);
  size_t mask = static_cast<size_t>(pow(2, bits)) - 1;
  size_t num_bits = *(size_t *)(&num) & mask;
  string output;

  output.resize(bits);

  for (size_t n = 0; n < bits; n++)
  {
    output[bits - n - 1] = (num_bits & 1 ? '1' : '0');
    num_bits >>= 1;
  }

  cout << output << endl;
}

unsigned long long reverse_long_double(long double ldnum, int count, int num)
{
  unsigned long long shift = (unsigned long long)num - (unsigned long long)count + 1;
  type in_long_double;
  in_long_double.d = ldnum;
  unsigned long long mask = ((1 << (unsigned long long)count) - 1) << shift;
  unsigned long long ext = (in_long_double.ll & mask) >> shift;
  unsigned long long rev_ext = 0;
  for (int i = 0; i < count; ++i)
  {
    rev_ext <<= 1;
    rev_ext |= ext & 1;
    ext >>= 1;
  }
  rev_ext <<= shift;

  return (in_long_double.ll & ~mask) | rev_ext;
}

unsigned int reverse_char(unsigned int num, int c, int n)
{
  int shift = n - c + 1;
  unsigned int mask = ((1 << c) - 1) << shift;
  unsigned int ext = (num & mask) >> shift;
  unsigned int rev_ext = 0;
  int i;
  for (i = 0; i < c; ++i)
  {
    rev_ext <<= 1;
    rev_ext |= ext & 1;
    ext >>= 1;
  }
  rev_ext <<= shift;

  return (num & ~mask) | rev_ext;
}

int main()
{
  string num;
  char chnum;
  long double ldnum;
  int i;
  char yes;

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

      chnum = (char)atoi(num.c_str());
      to_binary(chnum);

      cout << "Do you want to mirror some numbers? y/N" << endl;
      cin >> yes;

      if (yes == 'y')
      {
        int amount;
        int begin;
        cout << "Enter an amount of numbers to shuffle: ";
        scanf("%d", &amount);

        cout << "Enter an index to start with: ";
        scanf("%d", &begin);

        char reversed = reverse_char(chnum, amount, begin);
        printf("%u\n", reversed);
        to_binary(reversed);
      }

      break;

    case 2:
      cout << "Enter your long double: ";
      cin >> ldnum;
      cout << endl;

      to_binary(ldnum);

      cout << "Do you want to mirror some numbers? y/N" << endl;
      cin >> yes;

      if (yes == 'y')
      {
        int amount;
        int begin;
        long double result;

        cout << "Enter amount of numbers to shuffle: ";
        cin >> amount;
        cout << "Enter an index to start with: ";
        cin >> begin;

        result = reverse_long_double(ldnum, amount, begin);
        to_binary(result);
        cout << result << endl;
      }
      break;

    default:
      break;
    }

    return 0;
  }
}
