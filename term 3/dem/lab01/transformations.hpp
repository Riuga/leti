#include <iostream>
#include <cmath>

using namespace std;

const uint8_t BYTE_SIZE = 8;

template <typename T>
size_t to_binary(const T &num)
{
  const size_t bits = BYTE_SIZE * sizeof(num);
  size_t mask = static_cast<size_t>(pow(2, bits)) - 1;
  size_t num_bits = *(size_t *)(&num) & mask;

  cout << num_bits << endl;

  return num_bits;
}

template <typename T>
T partial_inverse(const T &src, uint8_t start, uint8_t len)
{
  uint8_t bits = sizeof(T) * BYTE_SIZE;
  uint8_t end = start + len < bits ? start + len : bits;
  T num = 0;

  for (uint8_t n = 0; n < bits; ++n)
  {
    __int128 mask = (*(__int128 *)&src >> n) & 1;

    if (n >= start && n < end)
    {
      mask = mask & 1 ? 0 : 1;
    }
    else
    {
      mask &= 1;
    }

    *(__int128 *)&num ^= mask << n;
  }

  cout << num << endl;

  return num;
}

template <typename T>
T to_decimal(T number)
{
  T num{};
  size_t bits = sizeof(T) * BYTE_SIZE;

  for (size_t i = 0; i < bits; ++i)
  {
    __int128 n = 1;
    number << 1;
    *(__int128 *)&num ^= (n << bits - i - 1);
  }

  cout << num << endl;

  return num;
}
