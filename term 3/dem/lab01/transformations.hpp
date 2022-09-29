#include <iostream>
#include <cmath>

using namespace std;

template <typename T>
string to_binary(const T &num)
{
  const int8_t BYTE_SIZE = 8;
  const size_t bits = BYTE_SIZE * sizeof(num);
  size_t mask = static_cast<size_t>(pow(2, bits)) - 1;
  size_t num_bits = *(size_t *)(&num) & mask;
  std::string output;

  output.resize(bits);

  for (size_t n = 0; n < bits; n++)
  {
    output[bits - n - 1] = (num_bits & 1 ? '1' : '0');
    num_bits >>= 1;
  }

  return output;
}

string mirror_shuffle(string number, int index, int amount)
{
  string output = number.data();
  int begin = number.length() - index;
  int end = begin + amount;

  if ((begin + amount - 1) > number.length() || number.length() < begin)
  {
    cout << "Incorrect input" << endl;
    return "";
  }

  for (int i = 0; i < amount / 2; i++)
  {
    output[begin] = number[end];
    output[end] = number[begin];
    begin++;
    end--;
  }

  return output;
}

template <typename T>
T to_decimal(const string &number)
{
  T num;

  auto last = number.end() - 1;
  void *p = calloc(sizeof(number.length()), 1);

  for (auto i = number.begin(); i != number.end(); i++)
  {
    *(long *)p += (*i == '1' ? 1 : 0);

    if (i != last)
    {
      *(long *)p <<= 1;
    }
  }

  num = *(T *)p;
  free(p);

  return num;
}
