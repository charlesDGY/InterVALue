/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/common.h
 *       @date         :  2015/03/26 15:19
 *       @description  :
 *
 *****************************************************************************/
#ifndef COMMON_H
#define COMMON_H
#include <stdio.h>
#include "interval.h"

//calculate the max of a and b
interval_value_type interval_value_max(interval_value_type a, interval_value_type b);
//calculate the min of a and b
interval_value_type interval_value_min(interval_value_type a, interval_value_type b);


void add_overflow(interval_value_type *a, interval_value_type *b) ;

void sub_overflow(interval_value_type *a, interval_value_type *b) ;

void mul_overflow(interval_value_type *a, interval_value_type *b) ;

void div_overflow(interval_value_type *a, interval_value_type *b) ;
//calculate the sum of a and b. Deal with the infinite number MAX_VALUE and MIN_VALUE, overflow error.
interval_value_type add_inf(interval_value_type a, interval_value_type b);

interval_value_type sub_inf(interval_value_type a, interval_value_type b);

interval_value_type mul_inf(interval_value_type a, interval_value_type b);

interval_value_type div_inf(interval_value_type a, interval_value_type b);
#endif
