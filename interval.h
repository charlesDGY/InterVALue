/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/interval.h
 *       @date         :  2015/03/26 09:24
 *       @description  :
 *
 *****************************************************************************/

#ifndef INTERVAL_H
#define INTERVAL_H


#include <stdio.h>
#include "common.h"
//basic interval type
typedef struct {
    interval_value_type low_value;
    interval_value_type up_value;
    //bool low_bound; [>true means close interval, false means open interval<]
    //bool up_bound;
} interval;


void interval_add(interval *a, interval *b, interval *c, int variable_type);

void interval_sub(interval *a, interval *b, interval *c, int variable_type);

void interval_mul(interval *a, interval *b, interval *c, int variable_type);

void interval_div(interval *a, interval *b, interval *c, int variable_type);

void interval_broaden(interval *a, interval *b, interval *c) ;

#endif
