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




struct edge_context {
    int name_d ;
    interval_node *value_set ;
//    value_t value_type ;
    edge_context *next ;
} ;




edge_context *make_context()
{
    edge_context *p = (edge_context *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("make context out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->name_d = -1 ;
    p->value_set = NULL ;
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


interval_node *search_node(interval_node *head, interval key)
{
    interval_node *p;
    for (p = head->next; p; p = p->next)
        if (p->item.low_value == key.low_value && p->item.up_value == key.up_value)
            return p;
    return NULL;
}





void insert_node(interval_node *head, interval_node *p)
{
    p->next = head->next;
    head->next = p;
}









//assume that all edge_context is originally generated to the same length and same variable sort.
edge_context *union_context(edge_context *head_a, edge_context *head_b) {
    if (head_a == NULL || head_b == NULL) {
        perror("union_context's input head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    //handle null and XN condition.
    if (head_a->next == NULL) {
        return copy_context(head_b) ;
    }
    if (head_b->next == NULL) {
        return copy_context(head_a) ;
    }

    edge_context *iter_a = NULL, *iter_b = NULL ;
    edge_context *context_p = NULL, *iter_r = NULL, *result = NULL ;
    iter_a = head_a->next ;
    iter_b = head_b->next ;

    //union set and set
    while (iter_a != NULL) {
        iter_r = new_context() ;
        iter_r->name_d = iter_a->name_d ;
        iter_r->value_set = set_set_union(iter_a->value_set, iter_b->value_set) ;
        if (result == NULL) {
            result = iter_r ;
            context_p = result ;
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
