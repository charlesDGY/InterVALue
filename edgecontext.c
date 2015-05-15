/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/edgecontext.c
 *       @date         :  2015/03/31 10:13
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>
#include "edgecontext.h"


edge_context *make_context()
{
    edge_context *p = (edge_context *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("make context out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->name_d = -1 ;
    interval item ;
    item.low_value = 0 ;
    item.up_value = 0 ;
    p->value_set = make_node(item) ;
    p->next = NULL ;
    return p;
}


edge_context *copy_context(edge_context *src)
{
    if (src == NULL) {
        perror("copy context source input is NULL!!") ;
        exit(EXIT_FAILURE) ;
    }

    interval temp_interval ;
    interval_node *iter = NULL, *result = NULL, *p = NULL ;

    edge_context *context_iter = NULL ;
    edge_context *context_p = NULL ;
    edge_context *temp_context = NULL ;
    edge_context *context_result = NULL ;

    context_iter = src ;

    while (context_iter != NULL) {
        temp_context = make_context() ;
        temp_context->name_d = context_iter->name_d ;

        iter = context_iter->value_set ;
        if (iter == NULL) {
            perror("copy_context's context value_set is NULL!!") ;
            exit(EXIT_FAILURE) ;
        }
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

        temp_context->value_set = result ;

        if (context_result == NULL) {
            context_result = temp_context ;
            context_p = context_result ;
        }
        else {
            context_p->next = temp_context ;
            context_p = context_p->next ;
        }
        context_iter = context_iter->next ;
    }

    return context_result ;
}


void destroy_context(edge_context *head)
{
    edge_context *q, *p = head;
    while (p) {
        q = p;
        p = p->next;
        destroy_set(q->value_set);
        free(q) ;
    }
}


void free_context_node(edge_context *p) {
    destroy_set(p->value_set) ;
    free(p);
}

edge_context *get_var(int var_name, edge_context *context) {
    if (context == NULL) {
        perror("get var wrong, context is null!!") ;
        exit(EXIT_FAILURE) ;
    }
    edge_context *pointer = NULL ;
    pointer = context ;
    while (pointer->next != NULL) {
        pointer = pointer->next ;
        if (pointer->name_d == var_name) {
            return pointer ;
        }
    }
    perror("get var wrong, no var name exist!!") ;
    exit(EXIT_FAILURE) ;
}

//estimate whether two edge_context is equal.
bool is_context_equal(edge_context *a, edge_context *b) {
    if (a == NULL || b == NULL) {
        perror("is_context_equal input a or b is NULL") ;
        exit(EXIT_FAILURE) ;
    }
    edge_context *pointer_a = NULL ;
    edge_context *pointer_b = NULL ;
    pointer_a = a ;
    pointer_b = b ;
    if (pointer_a->next == pointer_b->next && pointer_a->next == NULL) {
        return true ;
    }
    else if (pointer_a->next == NULL || pointer_b->next == NULL) {
        return false ;
    }
    while (pointer_a->next != NULL) {
        pointer_a = pointer_a->next ;
        pointer_b = pointer_b->next ;
        if (is_set_equal(pointer_a->value_set, pointer_b->value_set) == false) {
            return false ;
        }
    }
    return true ;
}


edge_context *broaden_context(edge_context *head_a, edge_context *head_b) {
    if (head_b == NULL) {
        perror("broaden_context's input head_b is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    //handle null and XN condition.
    if (head_a == NULL) {
        head_a = make_context() ;
    }

    if (head_a->next == NULL) {
        return copy_context(head_b) ;
    }
    if (head_b->next == NULL) {
        perror("broaden_context's input head_b->next is NULL!") ;
        exit(EXIT_FAILURE) ;
    }

    edge_context *iter_a = NULL, *iter_b = NULL ;
    edge_context *context_p = NULL, *iter_r = NULL, *result = NULL ;
    iter_a = head_a->next ;
    iter_b = head_b->next ;

    //broaden set and set
    while (iter_a != NULL) {
        iter_r = make_context() ;
        iter_r->name_d = iter_a->name_d ;
        if (is_set_equal(iter_a->value_set, iter_b->value_set) == false) {
            iter_r->value_set = set_set_broaden(iter_a->value_set, iter_b->value_set) ;
        }
        else {
            iter_r->value_set = copy_set(iter_a->value_set) ;
        }
        if (result == NULL) {
            result = make_context() ;
            result->next = iter_r ;
            context_p = result->next ;
        }
        else {
            context_p->next = iter_r ;
            context_p = context_p->next ;
        }
        iter_a = iter_a->next ;
        iter_b = iter_b->next ;
    }
    return result ;

}
