/*******************************************************************************
 *
 * Chronos: A Timing Analyzer for Embedded Software
 * =============================================================================
 * http://www.comp.nus.edu.sg/~rpembed/chronos/
 *
 * Copyright (C) 2005 Xianfeng Li
 *
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation; either version 2, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * $Id: cfg.h,v 1.2 2006/06/24 08:54:56 lixianfe Exp $
 *
 ******************************************************************************/

#ifndef CFG_H
#define CFG_H


#include <stdio.h>
#include "edgecontext.h"


#define NOT_TAKEN	0
#define TAKEN		1
#define BOTH_BRANCHES	2
#define LOOP_HEAD	1
#define LOOP_TAIL	2


typedef enum {DECLARATION, ASSIGNMENT, IF_TEST, SWITCH_TEST, JUNCTION, CALL, UNKNOWN_CALL} node_type_t ;

typedef struct declaration_t declaration_t ;
typedef struct assignment_t assignment_t ;
typedef struct if_test_t if_test_t ;
typedef struct switch_test_t switch_test_t ;
typedef struct junction_t junction_t ;
typedef struct call_t call_t ;
//typedef struct switch_chain switch_chain ;
typedef struct call_argument call_argument ;

struct declaration_t {
    char *name ;
    char *variable_type ;
    bool is_pointer ;
    bool is_array ;
    bool is_struct ;
    int array_len ;
}

struct assignment_t {
    char *dst_name ;
    char *operator_a ;
    char *operator_b ;
    char *operand ;
    bool is_type_convert ;     //if is_type_convert is true, operator_a saves the type to convert, operator_b saves the src variable.
}

struct if_test_t {
    char *cmp_a ;
    char *cmp_b ;
    char *cmp_operand ;
}

/*struct switch_chain {*/
    /*int case_num ;*/
    /*switch_chain *next ;*/
/*}*/

struct switch_test_t {
    char *switch_value ;
//    switch_chain *case_chain ;     //the first case_chain member corresponding to the first succ_edges, default branch corresponding to the last succ_edges.
    int *case_chain ;
}

struct junction_t {
    bool is_simple_junction ;
}

struct call_argument {
    char *arg_name ;
    char *arg_type ;
    call_argument *next ;
}

struct call_t {
    char *dst_name ;
    char *call_name ;
    call_argument *input_chain ;
}




typedef struct cfg_edge_t cfg_edge_t ;
typedef struct cfg_node_t cfg_node_t ;
typedef struct cfg_func_t cfg_func_t ;

struct cfg_edge_t {
    int edge_id ;
    cfg_node_t *start_node ;
    cfg_node_t *end_node ;
    edge_context *context_set ;
//    cfg_edge_t *next ;
}


struct cfg_node_t {
    int node_id ;
    int pre_edges_num ;
    int succ_edges_num ;
    cfg_edge_t **pre_edges ;
    cfg_edge_t **succ_edges ;
    node_type_t node_type ;
    declaration_t *declaration_i ;
    assignment_t *assignment_i ;
    if_test_t *if_test_i ;
    switch_test_t *switch_test_i ;
    junction_t *junction_t ;
    call_t *call_i ;

}

struct cfg_func_t {
    char *func_name ;
    call_argument *input_argument ;
    cfg_edge_t *pre_entry ;
}

/*// control flow graph node (basic block) type*/
/*typedef struct {*/
    /*int		id;		// basic block id (per procedure)*/
    /*proc_t  	*proc;		// up-link to the procedure containing it*/
    /*addr_t	sa;		// block start addr*/
    /*int		size;		// size (in bytes)*/
    /*int		num_inst;	// number of instructions*/
    /*de_inst_t   *code;		// pointer to the first instruction*/

    /*bb_type_t	type;*/
    /*cfg_edge_t	*out_n, *out_t;	// outgoing edges (non-taken/taken)*/
    /*int		num_in;		// number of incoming edges*/
    /*cfg_edge_t	**in;		// incoming edges*/

    /*proc_t	*callee;	// points to a callee if callee_addr not NULL*/

    /*int		loop_role;	// whether it is a loop head, tail, or neither*/

    /*int		flags;		// for traverse usage*/

    /*[> A data structure holding abstract register <]*/
    /*ric_p* in_abs_reg_value;	[> values. Register numbers can directly be <]*/
    /*ric_p* out_abs_reg_value; [> indexed in this structure <]*/

    /*abs_mem_p in_abs_mem_value;  [> A data structure holding value in abstract <]*/
    /*abs_mem_p out_abs_mem_value; [>  memory locations <]*/


    /*[>** HBK: for scope-aware data cache analysis **<]*/
    /*void   *d_instlist;*/
    /*int    num_d_inst;*/

/*} cfg_node_t;*/



/*// control flow graph edge type*/
/*struct cfg_edge_t {*/
    /*cfg_node_t  *src, *dst;	// src -> dst*/
/*};*/



/*// procedure type*/
/*struct proc_t {*/
    /*int		id;		// proc id*/
    /*addr_t	sa;		// proc start addr*/
    /*int		size;		// size (in bytes)*/
    /*int		num_inst;	// number of instructions*/
    /*de_inst_t   *code;		// instructions*/

    /*int		num_bb;		// number of basic blocks*/
    /*cfg_node_t	*cfg;		// cfg nodes with num_bb nodes*/

    /*int		flags;*/
/*};*/

/*// symbol table (address range of global variable*/
/*typedef struct {*/
    /*char* name;*/
    /*addr_t addr;*/
    /*int size;*/
/*} symbol_i;*/


/*//program type*/
/*typedef struct {*/
/*de_inst_t	*code;		// decoded program text*/
/*int		    code_size;	// code size (in bytes)*/
/*int		    num_inst;	// number of instructions*/
/*addr_t	    start_addr, end_addr, main_addr;*/
/*proc_t	    *procs;		// procedures*/
/*symbol_i    *p_info;    // procedure symbol info*/
/*symbol_i    *v_info;    // global variable symbol info*/
/*int         num_vars;   // number of global variables*/
/*int		    num_procs;	// number of procedures*/
/*int		    main_proc;	// index of the main proc*/
/*} prog_t;*/

/*#define MAX_OVRL_NODES 1024*/
/*#define OPT 1*/

/*struct col_data*/
/*{*/
/*union {*/
/*proc_t* proc;*/
/*de_inst_t* inst;*/
/*}u;*/
/*int type;*/
/*struct col_data* next;*/
/*};*/

/*typedef struct col_data* col_data_p;*/
/*typedef struct col_data col_data_s;*/

/*[> Describes the data structures used for layout formation <]*/
/*struct ovrl_graph {*/
/*union {*/
/*proc_t* proc;*/
/*de_inst_t* inst;*/
/*col_data_p pref;*/
/*}u;*/
/*int type;*/
/*int invalid;*/
/*[> execution count by WCET <]*/
/*int freq;*/
/*struct ovrl_graph* next;*/
/*};*/
/*typedef struct ovrl_graph* ovrl_graph_p;*/
/*typedef struct ovrl_graph ovrl_graph_s;*/


/*void*/
/*dump_cfg(FILE *fp, proc_t *proc);*/



#endif
