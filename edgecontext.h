/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/edgecontext.h
 *       @date         :  2015/03/31 10:13
 *       @description  :
 *
 *****************************************************************************/

#ifndef EDGECONTEXT_H
#define EDGECONTEXT_H

#include "intervalset.h"

//typedef enum {NUM, BOOL} value_t ;

typedef struct edge_context edge_context ;



struct edge_context {
    int name_d ;
    interval_node *value_set ;
//    value_t value_type ;
    edge_context *next ;
} ;


edge_context *make_context() ;


edge_context *copy_context(edge_context *src) ;

void destroy_context(edge_context *head) ;

void free_context_node(edge_context *p) ;

//assume that all edge_context is originally generated to the same length and same variable sort.

edge_context *get_var(int var_name, edge_context *context) ;

//estimate whether two edge_context is equal.
bool is_context_equal(edge_context *a, edge_context *b) ;

edge_context *broaden_context(edge_context *head_a, edge_context *head_b) ;


















#endif
