/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/interval.c
 *       @date         :  2015-04-08 11:14
 *       @description  :
 *
 *****************************************************************************/


#include <stdio.h>
#include <math.h>
#include "interval.h"
#include "common.h"


void interval_add(interval *a, interval *b, interval *c) {
    if (a->low_value > MIN_VALUE && a->up_value > MIN_VALUE && b->low_value > MIN_VALUE && b->up_value > MIN_VALUE &&
            a->low_value < MAX_VALUE && a->up_value < MAX_VALUE && b->low_value < MAX_VALUE && b->up_value < MAX_VALUE) {
        c->low_value = add_inf(a->low_value, b->low_value) ;
        c->up_value = add_inf(a->up_value, b->up_value) ;
    }
    else if ((a->up_value == MAX_VALUE || b->up_value == MAX_VALUE) &&
            !((a->low_value == MIN_VALUE && b->low_value == MAX_VALUE) || (a->low_value == MAX_VALUE && b->low_value == MIN_VALUE))) {
        c->low_value = add_inf(a->low_value, b->low_value) ;
        c->up_value = MAX_VALUE ;
    }
    else if ((a->low_value == MIN_VALUE || b->low_value == MIN_VALUE) &&
            !((a->up_value == MIN_VALUE && b->up_value == MAX_VALUE) || (a->up_value == MAX_VALUE && b->up_value == MIN_VALUE))) {
        c->low_value = MIN_VALUE ;
        c->up_value = add_inf(a->up_value, b->up_value) ;
    }
    else {
        c->low_value = MIN_VALUE ;
        c->up_value = MAX_VALUE ;
    }
} ;

void interval_sub(interval *a, interval *b, interval *c) {
    if (a->low_value > MIN_VALUE && a->up_value > MIN_VALUE && b->low_value > MIN_VALUE && b->up_value > MIN_VALUE &&
            a->low_value < MAX_VALUE && a->up_value < MAX_VALUE && b->low_value < MAX_VALUE && b->up_value < MAX_VALUE) {
        c->low_value = sub_inf(a->low_value, b->up_value) ;
        c->up_value = sub_inf(a->up_value, b->low_value) ;
    }
    else if ((a->up_value == MAX_VALUE || b->low_value == MIN_VALUE) &&
            !((a->low_value == MAX_VALUE && b->up_value == MAX_VALUE) || (a->low_value == MIN_VALUE && b->up_value == MIN_VALUE))) {
        c->low_value = sub_inf(a->low_value, b->up_value) ;
        c->up_value = MAX_VALUE ;
    }
    else if ((a->low_value == MIN_VALUE || b->up_value == MAX_VALUE) &&
            !((a->up_value == MAX_VALUE && b->low_value == MAX_VALUE) || (a->up_value == MIN_VALUE && b->low_value == MIN_VALUE))) {
        c->low_value = MIN_VALUE ;
        c->up_value = sub_inf(a->up_value, b->low_value) ;
    }
    else {
        c->low_value = MIN_VALUE ;
        c->up_value = MAX_VALUE ;
    }
} ;

void interval_mul(interval *a, interval *b, interval *c) {
    if ((a->up_value < 0 && b->low_value > 0) || (a->up_value < 0 && b->up_value < 0) ||
            (a->low_value > 0 && b->low_value > 0) || (a->low_value > 0 && b->up_value < 0) ||
            (a->low_value > MIN_VALUE && a->up_value > MIN_VALUE && b->low_value > MIN_VALUE && b->up_value > MIN_VALUE &&
             a->low_value < MAX_VALUE && a->up_value < MAX_VALUE && b->low_value < MAX_VALUE && b->up_value < MAX_VALUE)) {
        interval_value_type temp_max, temp_min, temp_mid;
        temp_min = interval_value_min(mul_inf(a->low_value, b->low_value), mul_inf(a->low_value, b->up_value)) ;
        temp_mid = interval_value_min(mul_inf(a->up_value, b->low_value), mul_inf(a->up_value, b->up_value)) ;
        temp_min = interval_value_min(temp_min, temp_mid) ;
        temp_max = interval_value_max(mul_inf(a->low_value, b->low_value), mul_inf(a->low_value, b->up_value)) ;
        temp_mid = interval_value_max(mul_inf(a->up_value, b->low_value), mul_inf(a->up_value, b->up_value)) ;
        temp_max = interval_value_max(temp_max, temp_mid) ;
        c->low_value = temp_min ;
        c->up_value = temp_max ;
    }
    else {
        c->low_value = MIN_VALUE ;
        c->up_value = MAX_VALUE ;
    }
};

//if the arguments are float, just wipe out the floor and ceil function from the body.
void interval_div(interval *a, interval *b, interval *c) {
    if ((b->low_value > MIN_VALUE && b->up_value < 0) || (b->low_value > 0 && b->up_value < MAX_VALUE)) {
        interval_value_type temp_max, temp_min, temp_mid;
        temp_min = interval_value_min((interval_value_type)((double)a->low_value / b->low_value),
                (interval_value_type)((double)a->low_value / b->up_value)) ;
        temp_mid = interval_value_min((interval_value_type)((double)a->up_value / b->low_value),
                (interval_value_type)((double)a->up_value / b->up_value)) ;
        temp_min = interval_value_min(temp_min, temp_mid) ;
        temp_max = interval_value_max((interval_value_type)((double)a->low_value / b->low_value),
                (interval_value_type)((double)a->low_value / b->up_value)) ;
        temp_mid = interval_value_max((interval_value_type)((double)a->up_value / b->low_value),
                (interval_value_type)((double)a->up_value / b->up_value)) ;
        temp_max = interval_value_max(temp_max, temp_mid) ;
        c->low_value = temp_min ;
        c->up_value = temp_max ;
    }
    else if (b->low_value <= 0 && b->up_value >= 0 && a->up_value < 0) {
        c->low_value = MIN_VALUE ;
        c->up_value = -a->low_value ;
    }
    else if (b->low_value <= 0 && b->up_value >=0 && a->low_value > 0) {
        c->low_value = -a->up_value ;
        c->up_value = MAX_VALUE ;
    }
    else {
        c->low_value = MIN_VALUE ;
        c->up_value = MAX_VALUE ;
    }
} ;

