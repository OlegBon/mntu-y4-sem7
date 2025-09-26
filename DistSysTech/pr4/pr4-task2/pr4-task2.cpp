#include <stdio.h>

int main()
{
#ifdef _OPENMP
    printf("OpenMP version: %d\n", _OPENMP);
#else
    printf("OpenMP is not supported by this compiler.\n");
#endif
    return 0;
}