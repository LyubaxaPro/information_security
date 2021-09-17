#include "encoding.h"

char *encoding(char *str) 
{
  int len = strlen(str);
  int key_len = strlen(KEY);
  char *new_str = new char[len];

    for (int i = 0; i < len; i++) {
      new_str[i] = str[i] ^ KEY[i % key_len + 1];
    }

    return new_str;
}
