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
#include <stdlib.h>

#include "interval.h"
#include "common.h"

typedef struct interval_node {
    interval item ;
    struct interval_node *next ;
} interval_node ;



interval_node *make_node(interval item) ;

void free_node(interval_node *p) ;
void destroy_set(interval_node *head) ;

interval_node *copy_set(interval_node *src) ;


interval_node *search_node(interval_node *head, interval key) ;


//interval_node *make_node(interval item);
//void free_node(interval_node *p);
//interval_node *search_node(interval key);
void insert_node(interval_node *head, interval_node *p) ;
//void delete_node(interval_node *p);
//void traverse(void (*visit)(interval_node *));
//void destroy_set(void);
//void push_node(interval_node *p);
//interval_node *pop_node(void);
//interval and set union operate
void interval_set_union(interval a, interval_node *head) ;

//interval and set intersect operate
void interval_set_intersect(interval a, interval_node *head) ;

//set and set union operate
interval_node *set_set_union(interval_node *head_a, interval_node *head_b) ;

//set and set intersect operate
interval_node *set_set_intersect(interval_node *head_a, interval_node *head_b) ;

interval_node *set_set_broaden(interval_node *head_a, interval_node *head_b) ;
//set and set add, sub, mul, div operate
interval_node *set_set_arithmetic(interval_node *head_a, interval_node *head_b, unsigned int operator_in, int variable_type) ;

//compulsory_convert of src to the result interval_node set
interval_node *compulsory_convert(interval_node *src, int variable_type) ;

interval_node *convert_to_set(interval_value_type src) ;


bool is_set_equal(interval_node *a, interval_node *b) ;




















#endif
