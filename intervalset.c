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



interval_node *make_node(interval item);
void free_node(interval_node *p);
interval_node *search_node(interval key);
void insert_node(interval_node *p);
void delete_node(interval_node *p);
void traverse(void (*visit)(interval_node *));
void destroy_node(void);
void push_node(interval_node *p);
interval_node *pop_node(void);



interval_node *make_node(interval item)
{
	interval_node *p = malloc(sizeof *p) ;
	p->item.low_value = item.low_value ;
    p->item.up_value = item.up_value ;
	p->next = NULL ;
	return p;
}

void free_node(interval_node *p)
{
	free(p);
}

interval_node *search_node(interval_node *head, interval key)
{
	interval_node *p;
	for (p = head->next; p; p = p->next)
		if (p->item.low_value == key.low_value && p->item.up_value == key.up_value)
			return p;
	return NULL;
}




//
void insert(interval_node * p)
{
	p->next = head;
	head = p;
}

void delete(interval_node *head, interval_node *p)
{
	interval_node *pre;
	if (p == head) {
		head = p->next;
		return;
	}
	for (pre = head; pre; pre = pre->next)
		if (pre->next == p) {
			pre->next = p->next;
			return;
		}
}

void traverse(void (*visit)(interval_node *))
{
	interval_node * p;
	for (p = head; p; p = p->next)
		visit(p);
}

void destroy_set(interval_node *head)
{
	interval_node *q, p = head;
	head = NULL;
	while (p) {
		q = p;
		p = p->next;
		free_node(q);
	}
}

void push(interval_node * p)
{
	insert(p);
}

interval_node * pop(void)
{
	if (head == NULL)
		return NULL;
	else {
		interval_node * p = head;
		head = head->next ;
		return p;
	}
}










//interval and set union operate
void interval_set_union(interval a, interval_node *head) {
    if (head->next == NULL) {
        head->next = make_node(a) ;
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

    interval_node *temp_node = NULL ;
    if (p != NULL && q == NULL) {
        temp_node = make_node(a) ;
        temp_node->next = head->next ;
        head->next = temp_node ;
    }
    else if (p == NULL && q != NULL) {
        q->next = make_node(a) ;
    }
    else if (p_loc > q_loc) {
        temp_node = make_node(a) ;
        q->next = temp_node ;
        temp_node->next = p ;
    }
    else {
        interval temp_interval ;
        temp_interval.low_value = interval_value_min(p->item.low_value, a.low_value) ;
        temp_interval.up_value = interval_value_max(q->item.up_value, a.up_value) ;
        temp_node = make_node(temp_interval) ;
        pre_p->next = temp_node ;
        temp_node->next = q->next ;
        q->next = NULL ;
        destroy_set(p) ;
    }
};

//interval and set intersect operate
void interval_set_intersect(interval a, interval_node *b) {

};


//set and set union operate
void set_set_union(interval_node *a, interval_node *b) ;

//set and set union operate
void set_set_intersect(interval_node *a, interval_node *b) ;

//set and set add, sub, mul, div operate
interval_node *set_set_arithmetic(interval_node *a, interval_node *b, unsigned int operator_in) ;







