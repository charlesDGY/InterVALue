/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/test/intervaltest.h
 *       @date         :  2015/04/01 15:58
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>

#define MIN -32768

typedef struct node {
    int i;
    int j;
    struct node *next;
} node;


int add(int a, int b) {
    printf("\n");
    return a + b ;
};

