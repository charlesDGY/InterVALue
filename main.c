/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/main.c
 *       @date         :  2015/03/24 20:13
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
//***************
#include "new_range_analysis.h"
//#include "rangeanalysis.h"

int main(int argc, const char *argv[])
{
    //char fName[256], str[256];
    /*strcpy(fName, argv[argc - 1]);*/
    /*if (argc <= 1) {*/
        /*fprintf(stderr, "parameter error!!\n");*/
        /*fprintf(stderr, "%s\n", argv[0]);*/
        /*exit(1);*/
    /*}*/

    //interval and interval calculate test
    //
    /*interval *a = (interval *)malloc(sizeof(interval)) ;*/
    /*interval *b = (interval *)malloc(sizeof(interval)) ;*/
    /*interval *c = (interval *)malloc(sizeof(interval)) ;*/
    /*a->low_value =  MIN_VALUE ;*/
    /*a->up_value = MAX_VALUE ;*/
    /*b->low_value = MIN_VALUE ;*/
    /*b->up_value = MIN_VALUE ;*/
    /*interval_add(a, b, c) ;*/
    /*printf("add:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_sub(a, b, c) ;*/
    /*printf("sub:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_mul(a, b, c) ;*/
    /*printf("mul:%ld %ld\n", c->low_value, c->up_value);*/
    /*interval_div(a, b, c) ;*/
    /*printf("div:%ld %ld\n", c->low_value, c->up_value);*/



    //interval_set calculate test
    //
    /*interval temp = {0, 0}, a = {0, 2}, b = {4, 6}, c = {8, 12}, d = {14, 17} ;*/
    /*int i = 0 ;*/
    /*interval_node *copy_head = NULL ;*/
    /*interval_node *head = make_node(temp) ;*/
    /*interval_node *iter = make_node(d) ;*/
    /*insert_node(head, iter) ;*/
    /*iter = make_node(c) ;*/
    /*insert_node(head, iter) ;*/
    /*iter = make_node(b) ;*/
    /*insert_node(head, iter) ;*/
    /*iter = make_node(a) ;*/
    /*insert_node(head, iter) ;*/
    /*iter = head->next ;*/
    /*printf("head: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/
    /*interval interval_temp = {18, 19} ;*/
    /*printf("interval :[%ld, %ld]\n", interval_temp.low_value, interval_temp.up_value);*/

    /*copy_head = copy_set(head) ;*/
    /*interval_set_union(interval_temp, copy_head) ;*/
    /*iter = copy_head->next ;*/
    /*printf("union: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/

    /*copy_head = copy_set(head) ;*/
    /*interval_set_intersect(interval_temp, copy_head) ;*/
    /*iter = copy_head->next ;*/
    /*printf("intersect: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("intersect :[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    //set and set calculate test

    /*interval temp_a = {0, 0}, a = {1, 6}, b = {7, 9}, c = {11, 13}, d = {14, 19} ;*/
    /*interval temp_b = {0, 0}, aa = {0, 2}, bb = {4, 6}, cc = {8, 12}, dd = {14, 17} ;*/
    /*interval_node *result_head = NULL ;*/
    /*interval_node *head_a = make_node(temp_a) ;*/
    /*interval_node *head_b = make_node(temp_b) ;*/
    /*interval_node *iter = make_node(d) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(c) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(b) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(a) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = head_a->next ;*/
    /*printf("head_a: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/

    /*iter = make_node(dd) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(cc) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(bb) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(aa) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = head_b->next ;*/
    /*printf("head_b: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    /*result_head = set_set_union(head_a, head_b) ;*/
    /*iter = result_head->next ;*/
    /*printf("union: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/

    /*result_head = set_set_intersect(head_a, head_b) ;*/
    /*iter = result_head->next ;*/
    /*printf("intersect: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    //set and set arithmetic -- add, sub, mul, div text
    //
    /*interval temp_a = {0, 0}, a = {1, 6}, b = {7, 9}, c = {11, 13}, d = {14, 19} ;*/
    /*interval temp_b = {0, 0}, aa = {1, 2}, bb = {2, 2}, cc = {2, 2}, dd = {14, 17} ;*/
    /*interval_node *result_head = NULL ;*/
    /*interval_node *head_a = make_node(temp_a) ;*/
    /*interval_node *head_b = make_node(temp_b) ;*/
    /*interval_node *iter = make_node(d) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(c) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(b) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = make_node(a) ;*/
    /*insert_node(head_a, iter) ;*/
    /*iter = head_a->next ;*/
    /*printf("head_a: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/

    /*iter = make_node(dd) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(cc) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(bb) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = make_node(aa) ;*/
    /*insert_node(head_b, iter) ;*/
    /*iter = head_b->next ;*/
    /*printf("head_b: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    /*result_head = set_set_arithmetic(head_a, head_b, 1) ;*/
    /*iter = result_head->next ;*/
    /*printf("add: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/

    /*result_head = set_set_arithmetic(head_a, head_b, 2) ;*/
    /*iter = result_head->next ;*/
    /*printf("sub: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    /*result_head = set_set_arithmetic(head_a, head_b, 3) ;*/
    /*iter = result_head->next ;*/
    /*printf("mul: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value);*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/


    /*result_head = set_set_arithmetic(head_a, head_b, 4) ;*/
    /*iter = result_head->next ;*/
    /*printf("div: ") ;*/
    /*while (iter != NULL) {*/
        /*printf("[%ld,%ld] ", iter->item.low_value, iter->item.up_value) ;*/
        /*iter = iter->next ;*/
    /*}*/
    /*printf("\n") ;*/
/*    //test function generation*/
    /*char *fp = "/home/dgy/Programming/VInterval/testfunc.c.gimple" ;*/
    /*char *glob_var_file = NULL ;*/
    /*cfg_func_t **result = NULL ;*/
    /*result = build_cfgs(fp, glob_var_file) ;*/
    /*int j = 0 ;*/
    /*while ((*result) != NULL) {*/
        /*printf("func_num: %d\n", (*result)->func_num) ;*/
        /*printf("func name: %s\n", (*result)->func_name) ;*/
        /*int i = 0 ;*/
        /*while ((*result)->input_argument[i] != NULL) {*/
            /*printf("input_argument %d : %s \nis_struct :%d \nis_pointer :%d \nstruct_name: %s\n",*/
                    /*(*result)->input_argument[i]->arg_type, (*result)->input_argument[i]->arg_name,*/
                    /*(*result)->input_argument[i]->is_struct,(*result)->input_argument[i]->is_pointer,(*result)->input_argument[i]->struct_name);*/
            /*i++ ;*/
        /*}*/
        /*result++ ;*/
    /*}*/
//
    //test cfg generation!
/*    char *fp = "/home/dgy/Programming/VInterval/usefultest.c.004t.gimple" ;*/
    /*char *glob_var_file = NULL ;*/
    /*cfg_func_t **result = NULL ;*/
    /*result = build_cfgs(fp, glob_var_file) ;*/
    /*int j = 0 ;*/
    /*while ((*result) != NULL) {*/
        /*printf("func_num: %d\n", (*result)->func_num) ;*/
        /*printf("func name: %s\n", (*result)->func_name) ;*/
        /*int i = 0 ;*/
        /*while ((*result)->input_argument[i] != NULL) {*/
            /*printf("input_argument %d : %s \nis_struct :%d \nis_pointer :%d \nstruct_name: %s\n",*/
                    /*(*result)->input_argument[i]->arg_type, (*result)->input_argument[i]->arg_name,*/
                    /*(*result)->input_argument[i]->is_struct,(*result)->input_argument[i]->is_pointer,(*result)->input_argument[i]->struct_name);*/
            /*i++ ;*/
        /*}*/
        /*result++ ;*/
    /*}*/

    /******************************************************************************************************************************************
    char *fp = "/home/dgy/Programming/VInterval/simpletest.c.004t.gimple" ;
    char *glob_var_file = NULL ;
    cfg_func_t **cfg_tree = NULL ;
    cfg_func_t **result_cfg = NULL ;
    cfg_tree = build_cfgs(fp) ;
    result_cfg = cfg_tree ;
    int j = 0 ;
    int i ;
    while ((*cfg_tree) != NULL) {
        printf("func_num: %d\n", (*cfg_tree)->func_num) ;
        printf("func name: %s\n", (*cfg_tree)->func_name) ;
        i = 0 ;
        while ((*cfg_tree)->input_argument[i] != NULL) {
            printf("input_argument %d : %s \nis_struct :%d \nis_pointer :%d \nstruct_name: %s\n",
                    (*cfg_tree)->input_argument[i]->arg_type, (*cfg_tree)->input_argument[i]->arg_name,
                    (*cfg_tree)->input_argument[i]->is_struct,(*cfg_tree)->input_argument[i]->is_pointer,(*cfg_tree)->input_argument[i]->struct_name);
            i++ ;
        }
        cfg_tree++ ;
    }

    //global
    interval_node *result_set = NULL ;
    edge_context *global_var_range = NULL ;
    global_var_range = get_global_context(result_cfg) ;

    //input i
    edge_context *func_actual_arg = NULL ;
    edge_context *input_i = NULL ;
    func_actual_arg = make_context() ;
    input_i = make_context() ;
    input_i->name_d = 0 ;
    interval item ;
    item.low_value = MIN_VALUE ;
    item.up_value = MAX_VALUE ;
    input_i->value_set->next = make_node(item) ;
    func_actual_arg->next = input_i ;

    result_set = range_analysis(global_var_range, func_actual_arg, i, result_cfg) ;

    return 0;
    **********************************************************************************************************************************************/
    char *fp = "/home/dgy/Programming/VInterval/codes/2_condition2.c.004t.gimple" ;
    char *action_fp = "/home/dgy/Programming/VInterval/codes/2_action2.c.004t.gimple" ;

    cfg_func_t **condition_cfg = NULL ;
    cfg_func_t **action_cfg = NULL ;

    int num = 1 ;
    condition_cfg = get_cfg(fp, &num) ;
    int i = 1 ;
    action_cfg = get_cfg(action_fp, &i) ;
    //input i
    edge_context *func_actual_arg = NULL ;
    edge_context *input_i = NULL ;
    func_actual_arg = make_context() ;
    input_i = make_context() ;
    input_i->name_d = 0 ;
    interval item ;
    item.low_value = 1 ;
    item.up_value = 1 ;
    input_i->value_set->next = make_node(item) ;
    func_actual_arg->next = input_i ;


    edge_context *end_context = NULL ;

    end_context = new_range_analysis(func_actual_arg, 0, condition_cfg, num) ;

    if (end_context->next != NULL) {
        printf("%f", end_context->next->value_set->next->item.low_value) ;
        printf("%f", end_context->next->value_set->next->item.up_value) ;


        end_context = new_range_analysis(end_context, 1, action_cfg, i) ;

        printf("%f", end_context->next->value_set->next->item.low_value) ;
        printf("%f", end_context->next->value_set->next->item.up_value) ;
    }

    return 0;

}
