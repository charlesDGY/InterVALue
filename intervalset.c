/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/intervalset.c
 *       @date         :  2015/03/29 08:47
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>

#include "intervalset.h"

/*typedef struct interval_node {*/
    /*interval item ;*/
    /*interval *next ;*/
/*} ;*/



interval_node *make_node(interval item)
{
    interval_node *p = malloc(sizeof *p) ;
    if (p == NULL) {
        perror("out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->item.low_value = item.low_value ;
    p->item.up_value = item.up_value ;
    p->next = NULL ;
    return p;
}

void free_node(interval_node *p)
{
    free(p);
}

void destroy_set(interval_node *head)
{
    interval_node *q, *p = head;
    while (p) {
        q = p;
        p = p->next;
        free_node(q);
    }
}


interval_node *copy_set(interval_node *src)
{
    if (src == NULL) {
        perror("source copy input is NULL!!") ;
        exit(EXIT_FAILURE) ;
    }
    interval temp_interval ;
    interval_node *iter = src, *result = NULL, *p = NULL ;

    temp_interval.low_value = iter->item.low_value ;
    temp_interval.up_value = iter->item.up_value ;
    result = make_node(temp_interval) ;
    p = result ;

    while (iter->next != NULL) {
        iter = iter->next ;
        temp_interval.low_value = iter->item.low_value ;
        temp_interval.up_value = iter->item.up_value ;
        p->next = make_node(temp_interval) ;
        p = p->next ;
    }
    return result ;
}


interval_node *search_node(interval_node *head, double key)
{
    interval_node *p;
    for (p = head->next; p; p = p->next)
        if (p->item.low_value <= key && p->item.up_value >= key)
            return p;
    return NULL;
}





void insert_node(interval_node *head, interval_node *p)
{
    p->next = head->next;
    head->next = p;
}

/*void delete(interval_node *head, interval_node *p)*/
/*{*/
/*interval_node *pre;*/
/*if (p == head) {*/
/*head = p->next;*/
/*return;*/
/*}*/
/*for (pre = head; pre; pre = pre->next)*/
/*if (pre->next == p) {*/
/*pre->next = p->next;*/
/*return;*/
/*}*/
/*}*/

/*void traverse(void (*visit)(interval_node *))*/
/*{*/
/*interval_node * p;*/
/*for (p = head; p; p = p->next)*/
/*visit(p);*/
/*}*/
/*void push(interval_node * p)*/
/*{*/
/*insert(p);*/
/*}*/

/*interval_node * pop(void)*/
/*{*/
/*if (head == NULL)*/
/*return NULL;*/
/*else {*/
/*interval_node * p = head;*/
/*head = head->next ;*/
/*return p;*/
/*}*/
/*}*/


//interval and set union operate, destroy old head and return new set in head.
void interval_set_union(interval a, interval_node *head) {
    if (head == NULL) {
        perror("input interval_set's head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    if (head->next == NULL) {
        head->next = make_node(a) ;
        return ;
    }
    interval_node *iter = NULL, *p = NULL, *q = NULL, *pre_p = NULL ;
    unsigned int p_loc = 0, q_loc = 0, i = 1 ;
    for (iter = head->next; iter; iter = iter->next) {
        //handle the condition that a's low_value is before first interval
        if (iter == head->next && a.low_value <= iter->item.up_value) {
            p = iter ;
            pre_p = head ;
            p_loc = i ;
        }
        //find a's low_value's interval in the head.
        else if (iter->next != NULL && a.low_value > iter->item.up_value && a.low_value <= (iter->next)->item.up_value) {
            p = iter->next ;
            pre_p = iter ;
            p_loc = i + 1 ;
        }
        //handle the condition that a's up_value is over the last interval
        if (iter->next == NULL && a.up_value >= iter->item.low_value) {
            q = iter ;
            q_loc = i ;
        }
        //find a's up_value's interval in the head
        else if (iter->next != NULL && a.up_value >= iter->item.low_value && a.up_value < (iter->next)->item.low_value) {
            q = iter ;
            q_loc = i ;
        }
        i++ ;
    }

    interval_node *temp_node = NULL ;
    //a is before the head
    if (p != NULL && q == NULL) {
        temp_node = make_node(a) ;
        temp_node->next = head->next ;
        head->next = temp_node ;
    }
    //a is over the head
    else if (p == NULL && q != NULL) {
        q->next = make_node(a) ;
    }
    //a is in the vacuum of two head's interval, directly insert a
    else if (p_loc > q_loc) {
        temp_node = make_node(a) ;
        q->next = temp_node ;
        temp_node->next = p ;
    }
    //a intersect head's some interval
    else {
        interval temp_interval ;
        temp_interval.low_value = interval_value_min(p->item.low_value, a.low_value) ;
        temp_interval.up_value = interval_value_max(q->item.up_value, a.up_value) ;
        temp_node = make_node(temp_interval) ;
        pre_p->next = temp_node ;
        temp_node->next = q->next ;
        q->next = NULL ;
        //free unuseful node
        destroy_set(p) ;
    }
}

//interval and set intersect operate, destroy old head and return new set in head
void interval_set_intersect(interval a, interval_node *head) {
/*    interval head_item ;*/
    /*head_item.low_value = 0 ;*/
    /*head_item.up_value = 0 ;*/
    /*interval_node *result = make_node(head_item) ;*/
    if (head == NULL) {
        perror("input interval_set's head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    if (head->next == NULL) {
        return ;
    }
    interval_node *iter = NULL, *p = NULL, *q = NULL, *pre_p = NULL ;
    unsigned int p_loc = 0, q_loc = 0, i = 1 ;
    for (iter = head->next; iter; iter = iter->next) {
        if (iter == head->next && a.low_value <= iter->item.up_value) {
            p = iter ;
            pre_p = head ;
            p_loc = i ;
        }
        else if (iter->next != NULL && a.low_value > iter->item.up_value && a.low_value <= (iter->next)->item.up_value) {
            p = iter->next ;
            pre_p = iter ;
            p_loc = i + 1 ;
        }
        if (iter->next == NULL && a.up_value >= iter->item.low_value) {
            q = iter ;
            q_loc = i ;
        }
        else if (iter->next != NULL && a.up_value >= iter->item.low_value && a.up_value < (iter->next)->item.low_value) {
            q = iter ;
            q_loc = i ;
        }
        i++ ;
    }

    //a doesn't intersect with head
    if ((p != NULL && q == NULL) || (p == NULL && q != NULL) || (p_loc > q_loc)) {
        destroy_set(head->next) ;
        head->next = NULL ;
        return ;
    }
    //a is enclosed by a interval of head
    else if (p == q) {
        interval_node *temp_node = NULL ;
        interval temp_interval ;
        temp_interval.low_value = interval_value_max(p->item.low_value, a.low_value) ;
        temp_interval.up_value = interval_value_min(q->item.up_value, a.up_value) ;
        temp_node = make_node(temp_interval) ;
        destroy_set(head->next) ;
        head->next = temp_node ;
        return ;
    }
    //a is intersect with some of the interval of head
    else {
        interval_node *temp_node_head = NULL, *temp_node_tail = NULL ;
        interval temp_head, temp_tail ;
        temp_head.low_value = interval_value_max(p->item.low_value, a.low_value) ;
        temp_head.up_value = p->item.up_value ;
        temp_tail.up_value = interval_value_min(q->item.up_value, a.up_value) ;
        temp_tail.low_value = q->item.low_value ;
        temp_node_head = make_node(temp_head) ;
        temp_node_tail = make_node(temp_tail) ;
        if (p->next != q) {
            temp_node_head->next = p->next ;
            iter = p ;
            while (iter->next != q) {
                iter = iter->next ;
            }
            iter->next = temp_node_tail ;
        }
        else {
            temp_node_head->next = temp_node_tail ;
        }
        p->next = NULL ;
        destroy_set(head->next) ;
        destroy_set(q) ;
        head->next = temp_node_head ;
        return ;
    }

}


//set and set union operate, no change head_a and head_b , return a new result use new dynamic space.
interval_node *set_set_union(interval_node *head_a, interval_node *head_b) {
    if (head_a == NULL || head_b == NULL) {
        perror("input interval_set's head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    //handle null and XN condition.
    if ((head_a->next == NULL) || (head_a->item.low_value == MIN_VALUE && head_a->item.up_value == MAX_VALUE)) {
        return copy_set(head_b) ;
    }
    if ((head_b->next == NULL) || (head_b->item.low_value == MIN_VALUE && head_b->item.up_value == MAX_VALUE)) {
        return copy_set(head_a) ;
    }
    interval_node *iter = NULL, *result = NULL ;
    result = copy_set(head_b) ;

    //union set and set
    iter = head_a->next ;
    while (iter != NULL) {
        interval_set_union(iter->item, result) ;
        iter = iter->next ;
    }
    return result ;
}

//set and set union operate, no change head_a and head_b, return a new result use new dynamic space.
interval_node *set_set_intersect(interval_node *head_a, interval_node *head_b) {
    if (head_a == NULL || head_b == NULL) {
        perror("input interval_set's head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    interval_node *iter = NULL, *temp_head = NULL, *result = NULL ;
    interval temp_interval ;
    temp_interval.low_value = 0 ;
    temp_interval.up_value = 0 ;
    result = make_node(temp_interval) ;

    if (head_a->item.low_value == MIN_VALUE && head_a->item.up_value == MAX_VALUE) {
        return copy_set(head_b) ;
    }
    else if (head_b->item.low_value == MIN_VALUE && head_b->item.up_value == MAX_VALUE) {
        return copy_set(head_a) ;
    }
    else if (head_a->next == NULL || head_b->next == NULL) {
        return result ;
    }
    iter = head_a->next ;

    //intersect set and set
    while (iter != NULL) {
        temp_head = copy_set(head_b) ;
        interval_set_intersect(iter->item, temp_head) ;
        result = set_set_union(temp_head, result) ;
        iter = iter->next ;
    }
    return result ;
}

interval_node *set_set_broaden(interval_node *head_a, interval_node *head_b) {
    if (head_a == NULL || head_b == NULL) {
        perror("set_set_broaden input head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    interval_node *iter = NULL, *result = NULL ;
    interval temp_interval ;
    interval a, b ;
    temp_interval.low_value = 0 ;
    temp_interval.up_value = 0 ;
    result = make_node(temp_interval) ;

    iter = head_a ;
    a.low_value = head_a->next->item.low_value ;
    while (iter->next != NULL) {
        iter = iter->next ;
    }
    a.up_value = iter->item.up_value ;
    iter = head_b ;
    b.low_value = head_b->next->item.low_value ;
    while (iter->next != NULL) {
        iter = iter->next ;
    }
    b.up_value = iter->item.up_value ;

    interval_broaden(&a, &b, &temp_interval) ;
    result->next = make_node(temp_interval) ;

    return result ;
}

//set and set add, sub, mul, div operate, 1 --add   2 -- sub  3 -- mul  4 -- div
interval_node *set_set_arithmetic(interval_node *head_a, interval_node *head_b, unsigned int operator_in, int variable_type) {
    if (head_a == NULL || head_b == NULL) {
        perror("input interval_set's head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    if (operator_in != 1 && operator_in != 2 && operator_in != 3 && operator_in != 4) {
        perror("operator_in must be from 1 to 4!") ;
        exit(EXIT_FAILURE) ;
    }
    interval_node *iter_a = NULL, *iter_b = NULL, *temp_head = NULL, *result = NULL ;
    interval temp_interval ;
    if ((head_a->item.low_value == MIN_VALUE && head_a->item.up_value == MAX_VALUE) ||
        (head_b->item.low_value == MIN_VALUE && head_b->item.up_value == MAX_VALUE)) {
        temp_interval.low_value = MIN_VALUE ;
        temp_interval.up_value = MAX_VALUE ;
        result = make_node(temp_interval) ;
        return result;
    }
    else if (head_a->next == NULL || head_b->next == NULL) {
        perror("input interval set's member is NULL, can't calculate set and set arithmetic!") ;
        exit(EXIT_FAILURE) ;
    }
    temp_interval.low_value = 0 ;
    temp_interval.up_value = 0 ;
    result = make_node(temp_interval) ;

    iter_a = head_a->next ;
    iter_b = head_b->next ;
    //calculate result
    while (iter_a != NULL) {
        while (iter_b != NULL) {
            //add
            if (operator_in == 1) {
                interval_add(&iter_a->item, &iter_b->item, &temp_interval, variable_type) ;
                interval_set_union(temp_interval, result) ;
            }
            //sub
            else if (operator_in == 2) {
                interval_sub(&iter_a->item, &iter_b->item, &temp_interval, variable_type) ;
                interval_set_union(temp_interval, result) ;
            }
            //mul
            else if (operator_in == 3) {
                interval_mul(&iter_a->item, &iter_b->item, &temp_interval, variable_type) ;
                interval_set_union(temp_interval, result) ;
            }
            //div
            else if (operator_in == 4) {
                interval_div(&iter_a->item, &iter_b->item, &temp_interval, variable_type) ;
                interval_set_union(temp_interval, result) ;
            }
            iter_b = iter_b->next ;
        }
        iter_b = head_b->next ;
        iter_a = iter_a->next ;
    }
    return result ;

}

interval_node *compulsory_convert(interval_node *src, int variable_type)
{
    if (src == NULL) {
        perror("source copy input is NULL!!") ;
        exit(EXIT_FAILURE) ;
    }
    interval temp_interval ;
    interval_node *iter = src, *result = NULL, *p = NULL ;

    temp_interval.low_value = iter->item.low_value ;
    temp_interval.up_value = iter->item.up_value ;
    result = make_node(temp_interval) ;
    p = result ;

    while (iter->next != NULL) {
        iter = iter->next ;
        if (variable_type == 0) {
            temp_interval.low_value = (int)iter->item.low_value ;
            temp_interval.up_value = (int)iter->item.up_value ;
        }
        else if (variable_type == 1) {
            temp_interval.low_value = (char)iter->item.low_value ;
            temp_interval.up_value = (char)iter->item.up_value ;
        }
        else if (variable_type == 2) {
            temp_interval.low_value = (short)iter->item.low_value ;
            temp_interval.up_value = (short)iter->item.up_value ;
        }
        else if (variable_type == 3) {
            temp_interval.low_value = (long)iter->item.low_value ;
            temp_interval.up_value = (long)iter->item.up_value ;
        }
        else if (variable_type == 4) {
            temp_interval.low_value = (long long)iter->item.low_value ;
            temp_interval.up_value = (long long)iter->item.up_value ;
        }
        else if (variable_type == 5) {
            temp_interval.low_value = (float)iter->item.low_value ;
            temp_interval.up_value = (float)iter->item.up_value ;
        }
        else if (variable_type == 6) {
            temp_interval.low_value = (double)iter->item.low_value ;
            temp_interval.up_value = (double)iter->item.up_value ;
        }
        else if (variable_type == 7) {
            temp_interval.low_value = (unsigned int)iter->item.low_value ;
            temp_interval.up_value = (unsigned int)iter->item.up_value ;
        }
        else if (variable_type == 8) {
            temp_interval.low_value = (unsigned char)iter->item.low_value ;
            temp_interval.up_value = (unsigned char)iter->item.up_value ;
        }
        else if (variable_type == 9) {
            temp_interval.low_value = (unsigned short)iter->item.low_value ;
            temp_interval.up_value = (unsigned short)iter->item.up_value ;
        }
        else if (variable_type == 10) {
            temp_interval.low_value = (unsigned long)iter->item.low_value ;
            temp_interval.up_value = (unsigned long)iter->item.up_value ;
        }
        else if (variable_type == 11) {
            temp_interval.low_value = (unsigned long long)iter->item.low_value ;
            temp_interval.up_value = (unsigned long long)iter->item.up_value ;
        }
        else {
            perror("unknown variable_type!!") ;
            exit(EXIT_FAILURE) ;
        }
        p->next = make_node(temp_interval) ;
        p = p->next ;
    }
    return result ;
}


interval_node *convert_to_set(interval_value_type src) {
    interval_node *result = NULL ;
    interval item ;
    item.low_value = 0 ;
    item.up_value = 0 ;
    result = make_node(item) ;

    item.low_value = src ;
    item.up_value = src ;
    result->next = make_node(item) ;
    return result ;
}



bool is_set_equal(interval_node *a, interval_node *b) {
    if (a == NULL || b == NULL) {
        perror("is_set_equal input a or b is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    interval_node *pointer_a = NULL ;
    interval_node *pointer_b = NULL ;
    pointer_a = a ;
    pointer_b = b ;
    while (pointer_a->next != NULL) {
        pointer_a = pointer_a->next ;
        pointer_b = pointer_b->next ;
        if (pointer_a->item.low_value != pointer_b->item.low_value || pointer_a->item.up_value != pointer_b->item.up_value) {
            return false ;
        }
    }
    return true ;
}


interval_node *split_set_low(interval_node *head, double key) {
    interval_node *result = NULL ;
    interval_node *key_node = NULL ;
    interval_node *pre_key_node = NULL ;
    double h_low, h_up ;
    h_low = head->next->item.low_value ;
    key_node = head ;
    while (key_node->next != NULL) {
        key_node = key_node->next ;
    }
    h_up = key_node->item.up_value ;

    if (h_up <= key) {
        result = copy_set(head) ;
        return result ;
    }
    if (h_low > key) {
        result = NULL ;
        return result ;
    }

    result = copy_set(head) ;

    key_node = result ;
    pre_key_node = key_node ;
    while (key_node->next != NULL) {
        key_node = key_node->next ;
        if (key_node->item.low_value <= key && key_node->item.up_value => key) {
            destroy_set(key_node->next) ;
            key_node->next = NULL ;
            key_node->item.up_value = key ;
        }
        else if (key_node->item.low_value > key && pre_key_node->item.up_value < key) {
            destroy_set(key_node) ;
            pre_key_node->next = NULL ;
        }
        pre_key_node = pre_key_node->next ;
    }
    return result ;
}

interval_node *split_set_up(interval_node *head, double key) {
    interval_node *result = NULL ;
    interval_node *key_node = NULL ;
    interval_node *pre_key_node = NULL ;
    interval item ;
    double h_low, h_up ;
    h_low = head->next->item.low_value ;
    key_node = head ;
    while (key_node->next != NULL) {
        key_node = key_node->next ;
    }
    h_up = key_node->item.up_value ;

    if (h_low >= key) {
        result = copy_set(head) ;
        return result ;
    }
    if (h_up < key) {
        result = NULL ;
        return result ;
    }

    item.low_value = 0 ;
    item.up_value = 0 ;
    result = make_node(item) ;

    key_node = head ;
    pre_key_node = key_node ;
    while (key_node->next != NULL) {
        key_node = key_node->next ;
        if (key_node->item.low_value <= key && key_node->item.up_value => key) {
            result->next = copy_set(key_node) ;
            result->next->item.low_value = key ;
        }
        else if (key_node->item.low_value > key && pre_key_node->item.up_value < key) {
            result->next = copy_set(key_node) ;
        }
        pre_key_node = pre_key_node->next ;
    }
    return result ;
}

