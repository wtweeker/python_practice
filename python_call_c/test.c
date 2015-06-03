#include <stdio.h>

int test(char *string)
{
  if(string != NULL)
  {
    printf("string: %s\n", string);
  }
  return 1;
}
