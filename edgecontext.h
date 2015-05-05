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

#include <stdio.h>
#include "intervalset.h"

//typedef enum {NUM, BOOL} value_t ;

typedef struct edge_context edge_context ;



struct edge_context {
    int name_d ;
    interval_node *value_set ;
//    value_t value_type ;
    edge_context *next ;
} ;






void free_node(edge_context *p) ;

void destroy_set(edge_context *head) ;

edge_context *copy_set(edge_context *src) ;

edge_context *search_node(edge_context *head, int name_d) ;


void insert_node(edge_context *head, edge_context *p) ;



edge_context *union_context(edge_context *head_a, edge_context *head_b) ;




















#endif
