#include <stdio.h>

int main(int argc, const char *argv[])
{
    int *a, b ;
    b = 5 ;
    a = &b ;
    printf("%d\n", *a);
    return 0 ;
}
