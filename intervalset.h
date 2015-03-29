/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/intervalset.h
 *       @date         :  2015/03/29 08:50
 *       @description  :
 *
 *****************************************************************************/

#ifndef INTERVALSET_H
#define INTERVALSET_H
#include <stdio.h>

#include "interval.h"
#include "common.h"

typedef struct interval_node {
    interval item ;
    interval *next ;
} ;



interval_node *make_node(interval item);
void free_node(interval_node *p);
interval_node *search_node(interval key);
void insert_node(interval_node *p);
void delete_node(interval_node *p);
void traverse(void (*visit)(interval_node *));
void destroy_set(void);
void push_node(interval_node *p);
interval_node *pop_node(void);


//interval and set union operate
interval_node *interval_set_union(interval a, interval_node *b) ;

//interval and set intersect operate
interval_node *interval_set_intersect(interval a, interval_node *b) ;


//set and set union operate
interval_node *set_set_union(interval_node *a, interval_node *b) ;

//set and set union operate
interval_node *set_set_intersect(interval_node *a, interval_node *b) ;

//set and set add, sub, mul, div operate
interval_node *set_set_arithmetic(interval_node *a, interval_node *b, unsigned int operator_in) ;


























#endif
