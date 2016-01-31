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
#include "rangeanalysis.h"
#include "new_range_analysis.h"


cfg_func_t **get_cfg(char *program_str, int *num) {

    char *fp = copy_string(program_str) ;
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
        i-- ;
        cfg_tree++ ;
    }

    *num = i ;
    return result_cfg ;

}

edge_context *new_range_analysis(edge_context *input_arg, int fp, cfg_func_t **result_cfg, int i)
{

    interval_node *result_set = NULL ;
    //global
    edge_context *global_var_range = NULL ;
    global_var_range = get_global_context(result_cfg) ;
    //input i
    edge_context *func_actual_arg = input_arg;
/*    edge_context *input_i = NULL ;
    func_actual_arg = make_context() ;
    input_i = make_context() ;
    input_i->name_d = 0 ;
    interval item ;
    item.low_value = MIN_VALUE ;
    item.up_value = MAX_VALUE ;
    input_i->value_set->next = make_node(item) ;
    func_actual_arg->next = input_i ;
*/
	edge_context *end_context = NULL ;
    end_context = make_context() ;
    /*char condition_update[] = "condition_update" ;*/
    /*if (strcmp(fp, condition_update) == 0) {*/
    if (fp == 0) {
        result_set = range_analysis_condition(global_var_range, func_actual_arg, i, result_cfg, end_context) ;
    }
    else {
        result_set = range_analysis(global_var_range, func_actual_arg, i, result_cfg, end_context) ;
    }

    return end_context;
}
