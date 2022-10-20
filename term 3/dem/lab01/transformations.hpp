#include <iostream>
#include <cmath>
#include <string>

using namespace std;

const uint8_t BYTE_SIZE = 8;

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

  to_binary(num);

  return num;
}

template <typename T>
void swap_bits(T &src, uint8_t pos1, uint8_t pos2)
{
  uint8_t bits = sizeof(T) * BYTE_SIZE;
  T tmp = src;

  for (uint8_t n = 0; n < bits; ++n)
  {
    __int128 bit{};

    if (n == pos1)
    {
      bit = (tmp >> pos2) & 1;
    }
    else if (n == pos2)
    {
      bit = (tmp >> pos1) & 1;
    }
    else
    {
      continue;
    }

    if (bit)
    { // bit == 1
      src |= (bit << n);
    }
    else
    { // bit == 0
      __int128 mask = 1;

      mask = (mask << bits) - 1;
      mask = partial_inverse(mask, n, 1);
      src &= mask;
    }
  }
}

template <typename T>
void mirror_range(T &src, uint8_t start, uint8_t len)
{
  uint8_t bits = sizeof(T) * BYTE_SIZE;
  uint8_t end = start + len < bits ? start + len : bits;
  uint8_t mid = (end + start) >> 1;

  for (uint8_t n = start; n < mid; ++n)
  {
    uint8_t x = (mid << 1) - n;
    if ((end + start) ^ 1)
    {
      x -= 1;
    }
    swap_bits(src, n, x);
  }
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
