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
        if (strcmp(current_node->assignment_i->operand, add_s) == 0) {
            operand = 1 ;
        }
        else if (strcmp(current_node->assignment_i->operand, sub_s) == 0) {
            operand = 2 ;
        }
        else if (strcmp(current_node->assignment_i->operand, mul_s) == 0) {
            operand = 3 ;
        }
        else if (strcmp(current_node->assignment_i->operand, div_s) == 0) {
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
    return result ;
}

edge_context *exec_if_test(cfg_node_t *current_node, edge_context *pre_context, cfg_func_t *function, edge_context *true_context, edge_context *false_context) {
    double a_d, b_d ;
    int a_i, b_i ;
    int cmp_operand ;
    bool a_low_c = false, a_up_c = false, b_low_c = false, b_up_c = false ;
    double a_low, a_up, b_low, b_up ;
    char l_s[] = ">", lq_s[] = ">=", s_s[] = "<", sq_s[] = "=<", eq_s[] = "==", nq_s[] = "!=" ;
    edge_context *pointer_a = NULL ;
    edge_context *pointer_b = NULL ;
    edge_context *f_pointer_a = NULL ;
    edge_context *f_pointer_b = NULL ;
    edge_context *result_true = NULL ;
    edge_context *result_false = NULL ;
    interval_node *node_pointer = NULL ;
    interval_node *node_pointer_b = NULL ;
    interval_node *f_node_pointer = NULL ;
    interval_node *f_node_pointer_b = NULL ;
    interval_node *temp_a = NULL ;
    interval_node *temp_b = NULL ;
    interval_node *temp_pre_node = NULL ;
    result_true = copy_context(pre_context) ;
    result_false = copy_context(pre_context) ;
    if (current_node->if_test_i->a_is_var == true && current_node->if_test_i->b_is_var == true) {
        a_i = atoi(current_node->if_test_i->cmp_a) ;
        b_i = atoi(current_node->if_test_i->cmp_b) ;
        pointer_a = get_var(a_i, result_true) ;
        pointer_b = get_var(b_i, result_true) ;
        f_pointer_a = get_var(a_i, result_false) ;
        f_pointer_b = get_var(b_i, result_false) ;
    }
    else if (current_node->if_test_i->a_is_var == true && current_node->if_test_i->b_is_var == false) {
        a_i = atoi(current_node->if_test_i->cmp_a) ;
        pointer_a = get_var(a_i, result_true) ;
        f_pointer_a = get_var(a_i, result_false) ;
        b_d = atof(current_node->if_test_i->cmp_b) ;
        pointer_b = make_context() ;
        destroy_set(pointer_b->value_set) ;
        pointer_b->value_set = convert_to_set(b_d) ;
        f_pointer_b = copy_context(pointer_b) ;
    }
    else {
        perror("exec_if_test cmp_a is not a var") ;
        exit(EXIT_FAILURE) ;
    }
    //get a_low and a_up, b_low and b_up
    a_low = pointer_a->value_set->next->item.low_value ;
    b_low = pointer_b->value_set->next->item.low_value ;
    temp_a = pointer_a->value_set ;
    while (temp_a->next != NULL) {
        temp_a = temp_a->next ;
    }
    a_up = temp_a->item.up_value ;
    temp_b = pointer_b->value_set ;
    while (temp_b->next != NULL) {
        temp_b = temp_b->next ;
    }
    b_up = temp_b->item.up_value ;
    //get result
    //> or >=
    if (strcmp(current_node->if_test_i->cmp_operand, l_s) == 0 || strcmp(current_node->if_test_i->cmp_operand, lq_s) == 0) {
        //true
        node_pointer = split_set_up(pointer_a->value_set, b_low) ;
        node_pointer_b = split_set_low(pointer_b->value_set, a_up) ;
        //if operand is > and variable_type is int class, sometimes the answer should be deleted some value.
        if (node_pointer->next != NULL && strcmp(current_node->if_test_i->cmp_operand, l_s) == 0 &&
            function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (node_pointer->next->item.low_value == node_pointer_b->next->item.low_value) {
                if (node_pointer->next->item.low_value == node_pointer->next->item.up_value) {
                    temp_a = node_pointer->next ;
                    node_pointer->next = node_pointer->next->next ;
                    free_node(temp_a) ;
                }
                else {
                    node_pointer->next->item.low_value++ ;
                }
            }
            if (node_pointer->next == NULL) {
                free_node(node_pointer_b->next) ;
                node_pointer_b->next = NULL ;
            }
            else {
                temp_a = node_pointer ;
                while (temp_a->next != NULL) {
                    temp_a = temp_a->next ;
                }
                temp_b = node_pointer_b ;
                temp_pre_node = temp_b ;
                while (temp_b->next != NULL) {
                    temp_b = temp_b->next ;
                    if (temp_b->next == NULL) {
                        break ;
                    }
                    temp_pre_node = temp_pre_node->next ;
                }
                if (temp_a->item.up_value == temp_b->item.up_value) {
                    if (temp_b->item.low_value == temp_b->item.up_value) {
                        temp_pre_node->next = NULL ;
                        free_node(temp_b) ;
                    }
                    else {
                        temp_b->item.up_value-- ;
                    }
                }
            }
        }
        //false
        f_node_pointer = split_set_low(f_pointer_a->value_set, b_up) ;
        f_node_pointer_b = split_set_up(f_pointer_b->value_set, a_low) ;

        if (f_node_pointer_b->next != NULL && strcmp(current_node->if_test_i->cmp_operand, lq_s) == 0 &&
                function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (f_node_pointer_b->next->item.low_value == f_node_pointer->next->item.low_value) {
                if (f_node_pointer_b->next->item.low_value == f_node_pointer_b->next->item.up_value) {
                    temp_b = f_node_pointer_b->next ;
                    f_node_pointer_b->next = f_node_pointer_b->next->next ;
                    free_node(temp_b) ;
                }
                else {
                    f_node_pointer_b->next->item.low_value++ ;
                }
            }

            if (f_node_pointer_b->next == NULL) {
                free_node(f_node_pointer->next) ;
                f_node_pointer->next = NULL ;
            }
            else {
                temp_b = f_node_pointer_b ;
                while (temp_b->next != NULL) {
                    temp_b = temp_b->next ;
                }
                temp_a = f_node_pointer ;
                temp_pre_node = temp_a ;
                while (temp_a->next != NULL) {
                    temp_a = temp_a->next ;
                    if (temp_a->next == NULL) {
                        break ;
                    }
                    temp_pre_node = temp_pre_node->next ;
                }

                if (temp_b->item.up_value == temp_a->item.up_value) {
                    if (temp_a->item.low_value == temp_a->item.up_value) {
                        temp_pre_node->next = NULL ;
                        free_node(temp_a) ;
                    }
                    else {
                        temp_a->item.up_value-- ;
                    }
                }

            }
        }
        /*if (a_up < b_low) {*/
        /*node_pointer = NULL ;*/
        /*}*/
        /*else if (a_low <= b_low && a_up >= b_up) {*/
        /*node_pointer = split_set_up(pointer_a->value_set, b_low) ;*/
        /*node_pointer_b = copy_set(pointer_b->value_set) ;*/
        /*}*/
        /*else if (a_low >= b_low && a_up >= b_up) {*/
        /*node_pointer = copy_set(pointer_a->value_set) ;*/
        /*node_pointer_b = copy_set(pointer_b->value_set) ;*/
        /*}*/
        /*else if (a_low < b_low && a_up < b_up) {*/
        /*node_pointer = split_set_up(pointer_a->value_set, b_low) ;*/
        /*node_pointer_b = split_set_low(pointer_b->value_set, a_up) ;*/
        /*}*/
        /*else if (a_low >= b_low && a_up <= b_up) {*/
        /*node_pointer = copy_set(pointer_a->value_set) ;*/
        /*node_pointer_b = split_set_low(pointer_b->value_set, a_up) ;*/
        /*}*/
    }
    //< or <=
    else if (strcmp(current_node->if_test_i->cmp_operand, s_s) == 0 || strcmp(current_node->if_test_i->cmp_operand, sq_s) == 0) {
        //true
        node_pointer = split_set_low(pointer_a->value_set, b_up) ;
        node_pointer_b = split_set_up(pointer_b->value_set, a_low) ;
        //if operand is < and variable_type is int class, sometimes the answer should be deleted some value.
        if (node_pointer_b->next != NULL && strcmp(current_node->if_test_i->cmp_operand, s_s) == 0 &&
                function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (node_pointer_b->next->item.low_value == node_pointer->next->item.low_value) {
                if (node_pointer_b->next->item.low_value == node_pointer_b->next->item.up_value) {
                    temp_b = node_pointer_b->next ;
                    node_pointer_b->next = node_pointer_b->next->next ;
                    free_node(temp_b) ;
                }
                else {
                    node_pointer_b->next->item.low_value++ ;
                }
            }

            if (node_pointer_b->next == NULL) {
                free_node(node_pointer->next) ;
                node_pointer->next = NULL ;
            }
            else {
                temp_b = node_pointer_b ;
                while (temp_b->next != NULL) {
                    temp_b = temp_b->next ;
                }
                temp_a = node_pointer ;
                temp_pre_node = temp_a ;
                while (temp_a->next != NULL) {
                    temp_a = temp_a->next ;
                    if (temp_a->next == NULL) {
                        break ;
                    }
                    temp_pre_node = temp_pre_node->next ;
                }

                if (temp_b->item.up_value == temp_a->item.up_value) {
                    if (temp_a->item.low_value == temp_a->item.up_value) {
                        temp_pre_node->next = NULL ;
                        free_node(temp_a) ;
                    }
                    else {
                        temp_a->item.up_value-- ;
                    }
                }

            }
        }
        //false
        f_node_pointer = split_set_up(f_pointer_a->value_set, b_low) ;
        f_node_pointer_b = split_set_low(f_pointer_b->value_set, a_up) ;

        if (f_node_pointer->next != NULL && strcmp(current_node->if_test_i->cmp_operand, sq_s) == 0 &&
                function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (f_node_pointer->next->item.low_value == f_node_pointer_b->next->item.low_value) {
                if (f_node_pointer->next->item.low_value == f_node_pointer->next->item.up_value) {
                    temp_a = f_node_pointer->next ;
                    f_node_pointer->next = f_node_pointer->next->next ;
                    free_node(temp_a) ;
                }
                else {
                    f_node_pointer->next->item.low_value++ ;
                }
            }
            if (f_node_pointer->next == NULL) {
                free_node(f_node_pointer_b->next) ;
                f_node_pointer_b->next = NULL ;
            }
            else {
                temp_a = f_node_pointer ;
                while (temp_a->next != NULL) {
                    temp_a = temp_a->next ;
                }
                temp_b = f_node_pointer_b ;
                temp_pre_node = temp_b ;
                while (temp_b->next != NULL) {
                    temp_b = temp_b->next ;
                    if (temp_b->next == NULL) {
                        break ;
                    }
                    temp_pre_node = temp_pre_node->next ;
                }
                if (temp_a->item.up_value == temp_b->item.up_value) {
                    if (temp_b->item.low_value == temp_b->item.up_value) {
                        temp_pre_node->next = NULL ;
                        free_node(temp_b) ;
                    }
                    else {
                        temp_b->item.up_value-- ;
                    }
                }
            }
        }
        /*if (b_up < a_low) {*/
            /*node_pointer = NULL ;*/
        /*}*/
        /*else if (b_low <= a_low && b_up >= a_up) {*/
            /*node_pointer_b = split_set_up(pointer_b->value_set, a_low) ;*/
            /*node_pointer = copy_set(pointer_a->value_set) ;*/
        /*}*/
        /*else if (b_low > a_low && b_up > a_up) {*/
            /*node_pointer_b = copy_set(pointer_b->value_set) ;*/
            /*node_pointer = copy_set(pointer_a->value_set) ;*/
        /*}*/
        /*else if (b_low < a_low && b_up < a_up) {*/
            /*node_pointer_b = split_set_up(pointer_b->value_set, a_low) ;*/
            /*node_pointer = split_set_low(pointer_a->value_set, b_up) ;*/
        /*}*/
        /*else if (b_low >= a_low && b_up <= a_up) {*/
            /*node_pointer_b = copy_set(pointer_b->value_set) ;*/
            /*node_pointer = split_set_low(pointer_a->value_set, b_up) ;*/
        /*}*/
    }
    //==
    else if (strcmp(current_node->if_test_i->cmp_operand, eq_s) == 0) {
        //true
        node_pointer = set_set_intersect(pointer_a->value_set, pointer_b->value_set) ;
        node_pointer_b = copy_set(node_pointer) ;
        //false
        if (function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (f_pointer_a->value_set->next->next == NULL && f_pointer_a->value_set->next->item.low_value == f_pointer_a->value_set->next->item.up_value) {
                f_node_pointer = copy_set(f_pointer_a->value_set) ;
                f_node_pointer_b = split_set_mid(f_pointer_b->value_set, f_pointer_a->value_set->next->item.low_value) ;
            }
            else if (f_pointer_b->value_set->next->next == NULL && f_pointer_b->value_set->next->item.low_value == f_pointer_b->value_set->next->item.up_value) {
                f_node_pointer = split_set_mid(f_pointer_a->value_set, f_pointer_b->value_set->next->item.low_value) ;
                f_node_pointer_b = copy_set(f_pointer_b->value_set) ;
            }
            else {
                f_node_pointer = copy_set(f_pointer_a->value_set) ;
                f_node_pointer_b = copy_set(f_pointer_b->value_set) ;
            }
        }
        else {
            f_node_pointer = copy_set(f_pointer_a->value_set) ;
            f_node_pointer_b = copy_set(f_pointer_b->value_set) ;
        }
    }
    else if (strcmp(current_node->if_test_i->cmp_operand, nq_s) == 0) {
        //true
        if (function->func_vars_table[a_i]->variable_type != 5 && function->func_vars_table[a_i]->variable_type != 6) {
            if (pointer_a->value_set->next->next == NULL && pointer_a->value_set->next->item.low_value == pointer_a->value_set->next->item.up_value) {
                node_pointer = copy_set(pointer_a->value_set) ;
                node_pointer_b = split_set_mid(pointer_b->value_set, pointer_a->value_set->next->item.low_value) ;
            }
            else if (pointer_b->value_set->next->next == NULL && pointer_b->value_set->next->item.low_value == pointer_b->value_set->next->item.up_value) {
                node_pointer = split_set_mid(pointer_a->value_set, pointer_b->value_set->next->item.low_value) ;
                node_pointer_b = copy_set(pointer_b->value_set) ;
            }
            else {
                node_pointer = copy_set(pointer_a->value_set) ;
                node_pointer_b = copy_set(pointer_b->value_set) ;
            }
        }
        else {
            node_pointer = copy_set(pointer_a->value_set) ;
            node_pointer_b = copy_set(pointer_b->value_set) ;
        }
        //false
        f_node_pointer = set_set_intersect(f_pointer_a->value_set, f_pointer_b->value_set) ;
        f_node_pointer_b = copy_set(f_node_pointer) ;
    }

    //update true and false succ_context
    destroy_set(pointer_a->value_set) ;
    pointer_a->value_set = node_pointer ;
    destroy_set(pointer_b->value_set) ;
    pointer_b->value_set = node_pointer_b ;
    destroy_set(f_pointer_a->value_set) ;
    f_pointer_a->value_set = f_node_pointer ;
    destroy_set(f_pointer_b->value_set) ;
    f_pointer_b->value_set = f_node_pointer_b ;

    if (node_pointer->next != NULL) {
        true_context->next = result_true->next ;
        free_context_node(result_true) ;
    }
    else {
        destroy_context(result_true) ;
    }
    if (f_node_pointer->next != NULL) {
        false_context->next = result_false->next ;
        free_context_node(result_false) ;
    }
    else {
        destroy_context(result_false) ;
    }
}

/*void add_context(edge_context *head, edge_context *new_context) {*/
    /*edge_context *pointer = NULL ;*/
    /*pointer = head ;*/
    /*while (pointer->next != NULL) {*/
        /*pointer = pointer->next ;*/
    /*}*/
    /*pointer->next = new_context ;*/
/*}*/

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

void creat_return_set(cfg_node_t *current_node, edge_context *current_context, interval_node *result) {
    int a_i ;
    double a_d ;
    interval_node *new_set = NULL ;
    interval_node *temp = NULL ;
    edge_context *pointer_a = NULL ;

    if (current_node->return_i->return_is_var == true) {
        a_i = atoi(current_node->return_i->return_num) ;
        pointer_a = get_var(a_i, current_context) ;
        new_set = copy_set(pointer_a->value_set) ;
    }
    else if (current_node->return_i->return_is_var == false) {
        a_d = atof(current_node->return_i->return_num) ;
        new_set = convert_to_set(a_d) ;
    }

    temp = set_set_union(result, new_set) ;
    destroy_set(result->next) ;
    result->next = temp->next ;
    free_node(temp) ;

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
    item.low_value = 0 ;
    item.up_value = 0 ;
    interval_node *result = NULL ;
    result = make_node(item) ;

    cfg_node_t *current_node = NULL ;
    cfg_edge_t *current_edge = NULL ;
    cfg_edge_t **pre_edges = NULL ;
    cfg_node_t **new_junction = NULL ;

    edge_context *current_context = NULL ;
    edge_context *succ_context = NULL ;
    edge_context *false_succ_context = NULL ;

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
    while (func_pointer->next != NULL) {
        func_pointer = func_pointer->next ;
        temp_context = make_context() ;
        temp_context->name_d = var_table - functions[func_num]->func_vars_table ;
        temp_context->value_set = copy_set(func_pointer->value_set) ;
        init_pointer->next = temp_context ;
        init_pointer = init_pointer->next ;
        var_table++ ;
    }

    while (global_pointer->next != NULL) {
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

    functions[func_num]->pre_entry->end_node->succ_edges[0]->context_set = initial_context ;
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
                succ_context = make_context() ;
                false_succ_context = make_context() ;
                exec_if_test(current_node, current_context, functions[func_num], succ_context, false_succ_context) ;
                if (succ_context->next != NULL) {
                    update_range(current_node->succ_edges[0], succ_context, edges, &edges_num) ;
                }
                else {
                    destroy_context(succ_context) ;
                }
                if (false_succ_context->next != NULL) {
                    update_range(current_node->succ_edges[1], false_succ_context, edges, &edges_num) ;
                }
                else {
                    destroy_context(false_succ_context) ;
                }
            }

            if (current_node->node_type == SWITCH_TEST) {
               /* for*/
                    /*succ*/
                    /*update*/
            }

            if (current_node->node_type == GOTO) {
                push_edges(current_node->succ_edges[0], edges, &edges_num) ;
                destroy_context(current_node->succ_edges[0]->context_set) ;
                current_node->succ_edges[0]->context_set = copy_context(current_context) ;
            }

            if (current_node->node_type == UNKNOWN_CALL) {
                push_edges(current_node->succ_edges[0], edges, &edges_num) ;
                destroy_context(current_node->succ_edges[0]->context_set) ;
                current_node->succ_edges[0]->context_set = copy_context(current_context) ;
            }

            if (current_node->node_type == RETURN) {
                creat_return_set(current_node, current_context, result) ;
                if (current_node->succ_edges[0]->end_node->node_type == EXIT) {
                    push_edges(current_node->succ_edges[0], edges, &edges_num) ;
                    destroy_context(current_node->succ_edges[0]->context_set) ;
                    current_node->succ_edges[0]->context_set = copy_context(current_context) ;
                }
            }

            if (current_node->node_type == EXIT) {
            }
        }
        //junctions
        for (new_junction = junctions; *new_junction != NULL; new_junction++) {
            succ_context = make_context() ;
            temp_context = NULL ;
            for (pre_edges = (*new_junction)->pre_edges; *pre_edges != NULL; pre_edges++) {
                if ((*pre_edges)->context_set == NULL) {
                    (*pre_edges)->context_set = make_context() ;
                }
                temp_context = union_context(succ_context, (*pre_edges)->context_set) ;
                destroy_context(succ_context) ;
                succ_context = temp_context ;
            }

            if ((*new_junction)->succ_edges[0]->context_set == NULL) {
                (*new_junction)->succ_edges[0]->context_set = make_context() ;
            }

            if (is_context_equal((*new_junction)->succ_edges[0]->context_set, succ_context) == false) {
                if ((*new_junction)->is_if_junction == true) {
                    update_range((*new_junction)->succ_edges[0], succ_context, edges, &edges_num) ;
                }
                else {
                    temp_context = broaden_context((*new_junction)->succ_edges[0]->context_set, succ_context) ;
                    update_range((*new_junction)->succ_edges[0], temp_context, edges, &edges_num) ;
                }
            }
        }

        //clear junctions
        junctions[0] = NULL ;
        junctions_num = 0 ;
    }
    return result ;
}
