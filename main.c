/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/main.c
 *       @date         :  2015/03/24 20:13
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "interval.h"

int main(int argc, const char *argv[])
{
	char fName[256], str[256];
    /*strcpy(fName, argv[argc - 1]);*/
    /*if (argc <= 1) {*/
        /*fprintf(stderr, "parameter error!!\n");*/
        /*fprintf(stderr, "%s\n", argv[0]);*/
        /*exit(1);*/
    /*}*/


    interval *a = (interval *)malloc(sizeof(interval)) ;
    interval *b = (interval *)malloc(sizeof(interval)) ;
    interval *c = (interval *)malloc(sizeof(interval)) ;
    a->low_value =  MIN_VALUE ;
    a->up_value = MAX_VALUE ;
    b->low_value = MIN_VALUE ;
    b->up_value = MIN_VALUE ;
    interval_add(a, b, c) ;
    printf("add:%ld %ld\n", c->low_value, c->up_value);
    interval_sub(a, b, c) ;
    printf("sub:%ld %ld\n", c->low_value, c->up_value);
    interval_mul(a, b, c) ;
    printf("mul:%ld %ld\n", c->low_value, c->up_value);
    interval_div(a, b, c) ;
    printf("div:%ld %ld\n", c->low_value, c->up_value);
    return 0;
}
