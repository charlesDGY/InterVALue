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




























#endif
