/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/rangeanalysis.c
 *       @date         :  2015/04/30 10:07
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>

#include "rangeanalysis.h"

//edges stack
void push_edges(cfg_edge_t *new_edge, cfg_edge_t **edges, int *edges_num) {
    edges[(*edges_num)] = new_edge ;              //consider copy the new_edge to handle recurse.
    (*edges_num)++ ;
    edges[(*edges_num)] = NULL ;
}

cfg_edge_t *pop_edges(cfg_edge_t **edges, int *edges_num) {
    cfg_edge_t *result = NULL ;
    if ((*edges_num) > 0) {
        (*edges_num)-- ;
        result = edges[(*edges_num)] ;
        edges[(*edges_num)] = NULL ;
    }
    return result ;
}

//junctions stack
void push_junctions(cfg_node_t *new_node, cfg_node_t **junctions, int *junctions_num) {
    junctions[(*junctions_num)] = new_node ;              //consider copy the new_edge to handle recurse.
    (*junctions_num)++ ;
    junctions[(*junctions_num)] = NULL ;
}

cfg_node_t *pop_junctions(cfg_node_t **junctions, int *junctions_num) {
    cfg_node_t *result = NULL ;
    if ((*junctions_num) > 0) {
        (*junctions_num)-- ;
        result = junctions[(*junctions_num)] ;
        junctions[(*junctions_num)] = NULL ;
    }
    return result ;
}

struct assignment_t {
    int dst_name ;
    char *operator_a ;
    char *operator_b ;
    char *operand ;
    bool is_type_convert ;     //if is_type_convert is true, operator_a saves the type to convert, operator_b saves the src variable.
    bool a_is_var ;
    bool b_is_var ;
    int has_array ;            //if dst is array, has_array == 1, if a is array, has_array == 2, if no array, has_array == 0.
    char *array_offset ;       //there will be at most one array within an assignment.
    bool offset_is_var ;
} ;

/*interval_value_type string_to_double(char *src) {*/

/*}*/

edge_context *exec_assignment(cfg_node_t *current_node, edge_context *pre_context, cfg_func_t *function) {
    double a_d, b_d ;
    int a_i, b_i, d_i ;
    int operand ;
    char add_s[] = "+", sub_s[] = "-", mul_s[] = "*", div_s[] = "/" ;
    edge_context *pointer = NULL ;
    edge_context *pointer_b = NULL ;
    edge_context *pointer_d = NULL ;
    edge_context *result = NULL ;
    interval_node *node_pointer = NULL ;
    result = copy_context(pre_context) ;
    d_i = current_node->assignment_i->dst_name ;
    pointer_d = get_var(d_i, result) ;

    if (current_node->assignment_i->is_type_convert == true) {
        a_i = atoi(current_node->assignment_i->operator_a) ;
        b_i = atoi(current_node->assignment_i->operator_b) ;
        pointer = get_var(b_i, result) ;
        node_pointer = compulsory_convert(pointer->value_set, a_i) ;
        destroy_set(pointer_d->value_set) ;
        pointer_d->value_set = node_pointer ;
    }
    //c[n] = a ;
    else if (current_node->assignment_i->has_array == 1) {

    }
    //c = a[n] ;
    else if (current_node->assignment_i->has_array == 2) {

    }
    //c = a
    else if (current_node->assignment_i->operator_b == NULL) {
        if (current_node->assignment_i->a_is_var == true) {
            a_i = atoi(current_node->assignment_i->operator_a) ;
            pointer = get_var(a_i, result) ;
            node_pointer = compulsory_convert(pointer->value_set, a_i) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
        else {
            a_d = atof(current_node->assignment_i->operator_a) ;
            node_pointer = convert_to_set(a_d) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
    }
    //c = a + b
    else {
        //operand
        if (strcmp(current_node->assignment_i->operand, add_s)) {
            operand = 1 ;
        }
        else if (strcmp(current_node->assignment_i->operand, sub_s)) {
            operand = 2 ;
        }
        else if (strcmp(current_node->assignment_i->operand, mul_s)) {
            operand = 3 ;
        }
        else if (strcmp(current_node->assignment_i->operand, div_s)) {
            operand = 4 ;
        }
        if (current_node->assignment_i->a_is_var == true && current_node->assignment_i->b_is_var == true) {
            a_i = atoi(current_node->assignment_i->operator_a) ;
            b_i = atoi(current_node->assignment_i->operator_b) ;
            pointer = get_var(a_i, result) ;
            pointer_b = get_var(b_i, result) ;
            node_pointer = set_set_arithmetic(pointer->value_set, pointer_b->value_set, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
        else if (current_node->assignment_i->a_is_var == true) {
            a_i = atoi(current_node->assignment_i->operator_a) ;
            pointer = get_var(a_i, result) ;

            b_d = atof(current_node->assignment_i->operator_b) ;
            node_pointer = convert_to_set(b_d) ;

            node_pointer = set_set_arithmetic(pointer->value_set, node_pointer, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
        else if (current_node->assignment_i->b_is_var == true) {
            b_i = atoi(current_node->assignment_i->operator_b) ;
            pointer = get_var(b_i, result) ;

            a_d = atof(current_node->assignment_i->operator_a) ;
            node_pointer = convert_to_set(a_d) ;

            node_pointer = set_set_arithmetic(node_pointer, pointer->value_set, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
        else {
            a_d = atof(current_node->assignment_i->operator_a) ;
            node_pointer = convert_to_set(a_d) ;
            b_d = atof(current_node->assignment_i->operator_b) ;
            node_pointer = convert_to_set(b_d) ;

        }
    }
}

void range_analysis(edge_context *input_var_range, edge_context *func_actual_arg, cfg_func_t *function, cfg_func_t **functions) {
    cfg_edge_t *edges[MAX_EDGE_STACK] ;
    int edges_num = 0 ;
    edges[0] = NULL ;
    cfg_node_t *junctions[MAX_JUNC_STACK] ;
    int junctions_num = 0 ;
    junctions[0] = NULL ;

    cfg_node_t *current_node = NULL ;
    cfg_edge_t *current_edge = NULL ;
    cfg_edge_t **pre_edges = NULL ;
    cfg_node_t **new_junction = NULL ;

    edge_context *current_context = NULL ;

    push_edges(function->pre_entry->end_node->succ_edges[0], edges, &edges_num) ;

    while (edges_num != 0) {
        while (edges_num != 0) {
            current_edge = pop_edges(edges, &edges_num) ;

            current_node = current_edge->end_node ;

            if (current_node->node_type == JUNCTION) {
                push_junctions(current_node, junctions, &junctions_num) ;
            }

            if (current_node->node_type == CALL) {

            }

            if (current_node->node_type == ASSIGNMENT) {

            }

            if (current_node->node_type == IF_TEST) {
                if (current_node->if_test_i->a_is_var == true) {
                    <`2`>
                }
            }

            if (current_node->node_type == SWITCH_TEST) {

            }

            if (current_node->node_type == GOTO) {
                push_edges(current_node->succ_edges[0], edges, &edge_num) ;
            }

            if (current_node->node_type == UNKNOWN_CALL) {
                push_edges(current_node->succ_edges[0], edges, &edge_num) ;
            }

            if (current_node->node_type == RETURN) {

            }

            if (current_node->node_type == EXIT) {

            }
        }

        //junctions
        for (new_junction = junctions; *new_junction != NULL; new_junction++) {
            for (pre_edges = new_junction->pre_edges; *pre_edges != NULL; pre_edges++) {

            }

            if (/* condition */) {
                <`2`>
            }
        }

        //clear junctions
        junctions[0] = NULL ;
        junctions_num = 0 ;
    }
}
