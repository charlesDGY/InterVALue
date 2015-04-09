/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/common.c
 *       @date         :  2015/03/26 15:09
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "common.h"

interval_value_type interval_value_max(interval_value_type a, interval_value_type b) {
    if (a > b) {
        return a ;
    } else {
        return b ;
    }
} ;


interval_value_type interval_value_min(interval_value_type a, interval_value_type b) {
    if (a < b) {
        return a ;
    } else {
        return b ;
    }
} ;

//handle add overflow
void add_overflow(interval_value_type *a, interval_value_type *b) {
    if (((*b > 0) && (*a > (MAX_VALUE - *b))) || ((*b < 0) && (*a < (MIN_VALUE - *b)))) {
    /* Handle error */
        perror("add overflow!") ;
        exit(EXIT_FAILURE) ;
    }
}

//add operator, consider the infinite and overflow.
interval_value_type add_inf(interval_value_type a, interval_value_type b) {
    if ((a == MAX_VALUE && b > MIN_VALUE && b < MAX_VALUE) || (b == MAX_VALUE && a > MIN_VALUE && a < MAX_VALUE) || (a == MAX_VALUE && b == MAX_VALUE) ) {
        return MAX_VALUE ;
    }
    else if ((a == MIN_VALUE && b > MIN_VALUE && b < MAX_VALUE) || (b == MIN_VALUE && a > MIN_VALUE && a < MAX_VALUE) || (a == MIN_VALUE && b == MIN_VALUE)) {
        return MIN_VALUE ;
    }
    else if ((a == MAX_VALUE && b == MIN_VALUE) || (a == MIN_VALUE && b == MAX_VALUE)) {
        perror("can't calculate different infinite add!") ;
        exit(EXIT_FAILURE);
    }
    else {
        add_overflow(&a, &b) ;
        return a + b ;
    }
}


//handle sub overflow
void sub_overflow(interval_value_type *a, interval_value_type *b) {
    if ((*b > 0 && *a < MIN_VALUE + *b) || (*b < 0 && *a > MAX_VALUE + *b)) {
        /* Handle error */
        perror("sub overflow!") ;
        exit(EXIT_FAILURE) ;
    }
}

//sub operator, consider the infinite and overflow
interval_value_type sub_inf(interval_value_type a, interval_value_type b) {
    if ((a == MAX_VALUE && b > MIN_VALUE && b < MAX_VALUE) || (b == MIN_VALUE && a > MIN_VALUE && a < MAX_VALUE) || (a == MAX_VALUE && b == MIN_VALUE)) {
        return MAX_VALUE ;
    }
    else if ((b == MAX_VALUE && a > MIN_VALUE && a < MAX_VALUE) || (a == MIN_VALUE && b > MIN_VALUE && b < MAX_VALUE) || (a == MIN_VALUE && b == MAX_VALUE)) {
        return MIN_VALUE ;
    }
    else if ((a == MAX_VALUE && b == MAX_VALUE) || (a == MIN_VALUE && b == MIN_VALUE)) {
        perror("can't calculate same infinite sub!") ;
        exit(EXIT_FAILURE) ;
    }
    else {
        sub_overflow(&a, &b) ;
        return a - b ;
    }
}

//handle mul overflow
void mul_overflow(interval_value_type *a, interval_value_type *b) {
    signed int result = 1 ;
    if (*a > 0) {  /* si_a is positive */
        if (*b > 0) {  /* si_a and si_b are positive */
            if (*a > (MAX_VALUE / *b)) {
                /* Handle error */
                result = -1 ;
            }
        } else { /* si_a positive, si_b nonpositive */
            if (*b < (MIN_VALUE / *a)) {
                /* Handle error */
                result = -1 ;
            }
        } /* si_a positive, si_b nonpositive */
    } else { /* si_a is nonpositive */
        if (*b > 0) { /* si_a is nonpositive, si_b is positive */
            if (*a < (MIN_VALUE / *b)) {
                /* Handle error */
                result = -1;
            }
        } else { /* si_a and si_b are nonpositive */
            if ((*a != 0) && (*b < (MAX_VALUE / *a))) {
                /* Handle error */
                result = -1;
            }
        } /* End if si_a and si_b are nonpositive */
    } /* End if si_a is nonpositive */
    if (result == -1) {
        perror("mul overflow!!") ;
        exit(EXIT_FAILURE) ;
    }
}

//mul operator, consider infinite and overflow
interval_value_type mul_inf(interval_value_type a, interval_value_type b) {
    if (a == MAX_VALUE) {
        if (b > 0) {
            return MAX_VALUE ;
        }
        else if (b < 0) {
            return MIN_VALUE ;
        }
    }
    else if (a == MIN_VALUE) {
        if (b > 0) {
            return MIN_VALUE ;
        }
        else if (b < 0) {
            return MAX_VALUE ;
        }
    }
    else if (b == MAX_VALUE) {
        if (a > 0) {
            return MAX_VALUE ;
        }
        else if (a < 0) {
            return MIN_VALUE ;
        }
    }
    else if (b == MIN_VALUE) {
        if (a > 0) {
            return MIN_VALUE ;
        }
        else if (a < 0) {
            return MAX_VALUE ;
        }
    }
    else {
        mul_overflow(&a, &b) ;
        return a * b ;
    }
}

//now can only handle int type, float type is ignored.
void div_overflow(interval_value_type *a, interval_value_type *b) {
    if ((*b == 0) || ((*a == MIN_VALUE) && (*b == -1))) {
        /* Handle error */
        perror("div overflow!") ;
        exit(EXIT_FAILURE) ;
    }
}

//now the function is not used because the interval_div function has the infinite handling.
interval_value_type div_inf(interval_value_type a, interval_value_type b) {
    if ((a == MAX_VALUE && b == MAX_VALUE) || (a == MAX_VALUE && b == MIN_VALUE) || (a == MIN_VALUE && b == MAX_VALUE) || (a == MIN_VALUE && b == MIN_VALUE)) {
        perror("can't calculate two infinite number's div!") ;
        exit(EXIT_FAILURE) ;
    }
    else if (b == MIN_VALUE || b == MAX_VALUE) {
        return 0 ;
    }
    else if ((a == MAX_VALUE && b > 0) || (a == MIN_VALUE && b < 0)) {
        return MAX_VALUE ;
    }
    else if ((a == MAX_VALUE && b < 0) || (a == MIN_VALUE && b > 0)) {
        return MIN_VALUE ;
    }
    else {
        div_overflow(&a, &b) ;
        return a / b ;
    }
}




//////////////////////////////////////////////////////
//file operate
//////////////////////////////////////////////////////


