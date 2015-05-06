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
    interval_node *node_pointer_b = NULL ;
    result = copy_context(pre_context) ;
    d_i = current_node->assignment_i->dst_name ;
    pointer_d = get_var(d_i, result) ;

    //type_convert
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
        //assignment
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
            node_pointer_b = convert_to_set(b_d) ;

            node_pointer = set_set_arithmetic(pointer->value_set, node_pointer_b, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
        else if (current_node->assignment_i->b_is_var == true) {
            b_i = atoi(current_node->assignment_i->operator_b) ;
            pointer = get_var(b_i, result) ;

            a_d = atof(current_node->assignment_i->operator_a) ;
            node_pointer = convert_to_set(a_d) ;

            node_pointer_b = set_set_arithmetic(node_pointer, pointer->value_set, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer_b ;
        }
        else {
            a_d = atof(current_node->assignment_i->operator_a) ;
            node_pointer = convert_to_set(a_d) ;
            b_d = atof(current_node->assignment_i->operator_b) ;
            node_pointer_b = convert_to_set(b_d) ;

            node_pointer = set_set_arithmetic(node_pointer, node_pointer_b, operand, function->func_vars_table[d_i]->variable_type) ;
            destroy_set(pointer_d->value_set) ;
            pointer_d->value_set = node_pointer ;
        }
    }
}


struct if_test_t {
    char *cmp_a ;
    char *cmp_b ;
    char *cmp_operand ;
    bool a_is_var ;
    bool b_is_var ;
} ;

edge_context *exec_if_test(cfg_node_t *current_node, edge_context *pre_context, cfg_func_t *function, bool if_true) {
    double a_d, b_d ;
    int a_i, b_i ;
    int cmp_operand ;
    char l_s[] = ">", lq_s[] = ">=", s_s[] = "<", sq_s[] = "=<", eq_s[] = "==" ;
    edge_context *pointer = NULL ;
    edge_context *pointer_b = NULL ;
    edge_context *result = NULL ;
    interval_node *node_pointer = NULL ;
    interval_node *node_pointer_b = NULL ;
    result = copy_context(pre_context) ;
    if (current_node->if_test_i->a_is_var == true && current_node->if_test_i->b_is_var == true) {
        a_i = atoi(current_node->assignment_i->cmp_a) ;
        pointer = get_var(a_i, result) ;
        destroy_set(pointer_d->value_set) ;
        pointer_d->value_set = node_pointer ;
    }
    else if (current_node->if_test_i->a_is_var == true && current_node->if_test_i->b_is_var == false) {

    }
    else {
        perror("exec_if_test cmp_a is not a var") ;
        exit(EXIT_FAILURE) ;
    }

    //c = a
    if (current_node->assignment_i->operator_b == NULL) {
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

}

void add_context(edge_context *head, edge_context *new_context) {
    edge_context *pointer = NULL ;
    pointer = head ;
    while (pointer->next != NULL) {
        pointer = pointer->next ;
    }
    pointer->next = new_context ;
}

void update_range(cfg_edge_t *new_edge, edge_context *new_context, cfg_edge_t **edges, int *edges_num) {
    edge_context *result = NULL ;
    if (new_edge->context_set == NULL) {
        new_edge->context_set = make_context() ;
    }
    if (is_context_equal(new_context, new_edge->context_set) == false) {
        result = union_context(new_edge->context_set, new_context) ;
        destroy_context(new_edge->context_set) ;
        destroy_context(new_context) ;
        new_edge->context_set = result ;

        push_edges(new_edge, edges, edges_num) ;
    }
}

interval_node *range_analysis(edge_context *global_var_range, edge_context *func_actual_arg, int func_num, cfg_func_t **functions) {
    if (global_var_range == NULL || func_actual_arg == NULL) {
        perror("range_analysis input global_var_range or func_actual_arg is NULL") ;
        exit(EXIT_FAILURE) ;
    }
    cfg_edge_t *edges[MAX_EDGE_STACK] ;
    int edges_num = 0 ;
    edges[0] = NULL ;
    cfg_node_t *junctions[MAX_JUNC_STACK] ;
    int junctions_num = 0 ;
    junctions[0] = NULL ;

    interval item ;

    cfg_node_t *current_node = NULL ;
    cfg_edge_t *current_edge = NULL ;
    cfg_edge_t **pre_edges = NULL ;
    cfg_node_t **new_junction = NULL ;

    edge_context *current_context = NULL ;
    edge_context *succ_context = NULL ;

    edge_context *initial_context = NULL ;
    edge_context *temp_context = NULL ;
    initial_context = make_context() ;
    edge_context *init_pointer = NULL ;
    init_pointer = initial_context ;

    edge_context *func_pointer = NULL ;
    edge_context *global_pointer = NULL ;
    func_pointer = func_actual_arg ;
    global_pointer = global_var_range ;

    declaration_t **var_table = NULL ;
    var_table = functions[func_num]->func_vars_table ;
    //set initial edge_context
    if (func_pointer->next != NULL) {
        func_pointer = func_pointer->next ;
        temp_context = make_context() ;
        temp_context->name_d = var_table - functions[func_num]->func_vars_table ;
        temp_context->value_set = copy_set(func_pointer->value_set) ;
        init_pointer->next = temp_context ;
        init_pointer = init_pointer->next ;
        var_table++ ;
    }

    if (global_pointer->next != NULL) {
        global_pointer = global_pointer->next ;
        temp_context = make_context() ;
        temp_context->name_d = var_table - functions[func_num]->func_vars_table ;
        //no copy_set, use global_var_range
        temp_context->value_set = global_pointer->value_set ;
        init_pointer->next = temp_context ;
        init_pointer = init_pointer->next ;
        var_table++ ;
    }

    while ((*var_table) != NULL) {
        temp_context = make_context() ;
        temp_context->name_d = var_table - functions[func_num]->func_vars_table ;
        item.low_value = 0 ;
        item.up_value = 0 ;
        temp_context->value_set = make_node(item) ;
        item.low_value = MIN_VALUE ;
        item.up_value = MAX_VALUE ;
        temp_context->value_set->next = make_node(item) ;
        init_pointer->next = temp_context ;
        init_pointer = init_pointer->next ;
        var_table++ ;
    }

    push_edges(functions[func_num]->pre_entry->end_node->succ_edges[0], edges, &edges_num) ;

    while (edges_num != 0) {
        while (edges_num != 0) {
            current_edge = pop_edges(edges, &edges_num) ;
            current_context = current_edge->context_set ;
            current_node = current_edge->end_node ;

            if (current_node->node_type == JUNCTION) {
                push_junctions(current_node, junctions, &junctions_num) ;
            }

            if (current_node->node_type == CALL) {

            }

            if (current_node->node_type == ASSIGNMENT) {
                succ_context = exec_assignment(current_node, current_context, functions[func_num]) ;
                update_range(current_node->succ_edges[0], succ_context, edges, &edges_num) ;
            }

            if (current_node->node_type == IF_TEST) {
                succ_context = exec_if_test(current_node, current_context, functions[func_num], true) ;
                update_range(current_node->succ_edges[0], succ_context, edges, &edges_num) ;
                succ_context = exec_if_test(current_node, current_context, functions[func_num], false) ;
                update_range(current_node->succ_edges[1], succ_context, edges, &edges_num) ;
            }

            if (current_node->node_type == SWITCH_TEST) {
               /* for*/
                    /*succ*/
                    /*update*/
            }

            if (current_node->node_type == GOTO) {
                push_edges(current_node->succ_edges[0], edges, &edge_num) ;
                destroy_context(current_node->succ_edges[0]->context_set) ;
                current_node->succ_edges[0]->context_set = copy_context(current_context) ;
            }

            if (current_node->node_type == UNKNOWN_CALL) {
                push_edges(current_node->succ_edges[0], edges, &edge_num) ;
                destroy_context(current_node->succ_edges[0]->context_set) ;
                current_node->succ_edges[0]->context_set = copy_context(current_context) ;
            }

            if (current_node->node_type == RETURN) {

            }

            if (current_node->node_type == EXIT) {
                return ;
            }
        }

        succ_context = make_context() ;
        temp_context = NULL ;
        //junctions
        for (new_junction = junctions; *new_junction != NULL; new_junction++) {
            for (pre_edges = new_junction->pre_edges; *pre_edges != NULL; pre_edges++) {
                temp_context = union_context(succ_context, pre_edges->context_set) ;
                destroy_context(succ_context) ;
                succ_context = temp_context ;
            }

            if (is_context_equal(new_junction->succ_edges[0]->context_set, succ_context) == false) {
                if (new_junction->is_if_junction == true) {
                    update_range(new_junction->succ_edges[0], succ_context, edges, &edges_num) ;
                }
                else {
                    temp_context = broaden_context(new_junction->succ_edges[0]->context_set, succ_context) ;
                    update_range(new_junction->succ_edges[0], temp_context, edges, &edges_num) ;
                }
            }
        }

        //clear junctions
        junctions[0] = NULL ;
        junctions_num = 0 ;
    }
}