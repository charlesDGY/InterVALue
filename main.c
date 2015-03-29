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
#include "intervalset.h"

int main(int argc, const char *argv[])
{
	char fName[256], str[256];
    /*strcpy(fName, argv[argc - 1]);*/
    /*if (argc <= 1) {*/
        /*fprintf(stderr, "parameter error!!\n");*/
        /*fprintf(stderr, "%s\n", argv[0]);*/
        /*exit(1);*/
    /*}*/

    //interval and interval calculate test
    /*interval *a = (interval *)malloc(sizeof(interval)) ;*/
    /*interval *b = (interval *)malloc(sizeof(interval)) ;*/
    /*interval *c = (interval *)malloc(sizeof(interval)) ;*/
    /*a->low_value =  MIN_VALUE ;*/
    /*a->up_value = MAX_VALUE ;*/
    /*b->low_value = MIN_VALUE ;*/
    /*b->up_value = MIN_VALUE ;*/
    /*interval_add(a, b, c) ;*/
    /*printf("add:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_sub(a, b, c) ;*/
    /*printf("sub:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_mul(a, b, c) ;*/
    /*printf("mul:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_div(a, b, c) ;*/
    /*printf("div:%ld %ld\n", c->low_value, c->up_value);*/



    //intervalset and intervalset calculate test
    interval temp = {0, 0}, a = {1, 2}, b = {4, 5}, c = {8, 12}, d = {14, 16} ;
    int i = 0 ;
    interval_node *copy_head = NULL ;
    interval_node *head = make_node(temp) ;
    interval_node *iter = make_node(d) ;
    insert_node(head, iter) ;
    iter = make_node(c) ;
    insert_node(head, iter) ;
    iter = make_node(b) ;
    insert_node(head, iter) ;
    iter = make_node(a) ;
    insert_node(head, iter) ;
    iter = head->next ;
    while (iter != NULL) {
        printf("head: [%ld,%ld] ", iter->item.low_value, iter->item.up_value);
        iter = iter->next ;
    }
   interval interval_temp = {1, 11} ;
    copy_head = copy_set(head) ;
    interval_set_union(interval_temp, copy_head) ;
    iter = copy_head->next ;
    while (iter != NULL) {
        printf("union :[%ld,%ld] ", iter->item.low_value, iter->item.up_value);
        iter = iter->next ;
    }
    copy_head = copy_set(head) ;
    interval_set_intersect(interval_temp, copy_head) ;
    iter = copy_head->next ;
    while (iter != NULL) {
        printf("intersect :[%ld,%ld] ", iter->item.low_value, iter->item.up_value);
        iter = iter->next ;
    }

    return 0;
}
