/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/rangeanalysis.h
 *       @date         :  2015/04/30 10:07
 *       @description  :
 *
 *****************************************************************************/

#ifndef RANGEANALYSIS_H
#define RANGEANALYSIS_H

#include "cfg.h"

#define MAX_EDGE_STACK 150
#define MAX_JUNC_STACK 150


void push_edges(cfg_edge_t *new_edge, cfg_edge_t **edges, int *edges_num) ;

cfg_edge_t *pop_edges(cfg_edge_t **edges, int *edges_num) ;

//junctions stack
void push_junctions(cfg_node_t *new_node, cfg_node_t **junctions, int *junctions_num) ;

cfg_node_t *pop_junctions(cfg_node_t **junctions, int *junctions_num) ;

edge_context *exec_assignment(cfg_node_t *current_node, edge_context *pre_context, cfg_func_t *function) ;

edge_context *exec_if_test(cfg_node_t *current_node, edge_context *pre_context, cfg_func_t *function, edge_context *true_context, edge_context *false_context) ;

void update_range(cfg_edge_t *new_edge, edge_context *new_context, cfg_edge_t **edges, int *edges_num) ;

void creat_return_set(cfg_node_t *current_node, edge_context *current_context, interval_node *result) ;

interval_node *range_analysis(edge_context *global_var_range, edge_context *func_actual_arg, int func_num, cfg_func_t **functions) ;

#endif
