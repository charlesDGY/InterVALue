/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/rangeanalysis.h
 *       @date         :  2015/04/30 10:07
 *       @description  :
 *
 *****************************************************************************/

#ifndef RANGEANALYSIS_H
#define RANGEANALYSIS_H


#include <stdio.h>
#include <float.h>

#include "cfg.h"
#include "edgecontext.h"

#define MAX_EDGE_STACK 150
#define MAX_JUNC_STACK 150

//basic interval type
typedef struct {
    interval_value_type low_value;
    interval_value_type up_value;
    //bool low_bound; [>true means close interval, false means open interval<]
    //bool up_bound;
} interval;


void interval_add(interval *a, interval *b, interval *c);

void interval_sub(interval *a, interval *b, interval *c);

void interval_mul(interval *a, interval *b, interval *c);

//div function can only handle non-float argument.
void interval_div(interval *a, interval *b, interval *c);

#endif
