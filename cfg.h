/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/cfg.h
 *       @date         :  2015/04/14 14:28
 *       @description  :
 *
 *****************************************************************************/

#ifndef CFG_H
#define CFG_H


#include <stdio.h>
#include "edgecontext.h"
#include "common.h"



#define MAX_FUNC_NUM 1000

#define MAX_FUNC_NAME 60

#define MAX_TYPE_NAME 60

#define MAX_INPUT_VAR 20

#define MAX_FUNC_VARS 1024

#define MAX_RANGE_DEPTH 20

#define MAX_LINE_LENGTH 2048

#define MAX_TOKEN_NUM 1024

#define MAX_EDGE_NUM 64


typedef enum {ENTRY, RETURN, GOTO, EXIT, DECLARATION, ASSIGNMENT, IF_TEST, SWITCH_TEST, JUNCTION, CALL, UNKNOWN_CALL} node_type_t ;

typedef struct declaration_t declaration_t ;
typedef struct assignment_t assignment_t ;
typedef struct if_test_t if_test_t ;
typedef struct switch_test_t switch_test_t ;
//typedef struct junction_t junction_t ;
typedef struct call_t call_t ;
//typedef struct switch_chain switch_chain ;
typedef struct call_argument call_argument ;
typedef struct call_parameter call_parameter ;
typedef struct token_list token_list ;
typedef struct return_t return_t ;
//typedef struct func_vars func_vars ;

typedef struct cfg_edge_t cfg_edge_t ;
typedef struct cfg_node_t cfg_node_t ;
typedef struct cfg_func_t cfg_func_t ;


struct declaration_t {
    char *name ;
    int variable_type ;
    bool is_pointer ;
    bool is_array ;
    bool is_struct ;        // if is struct , the type number is 13
    char *struct_name ;
    bool is_static ;
    int array_len ;
    int effect_domain ;
} ;

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

struct if_test_t {
    char *cmp_a ;
    char *cmp_b ;
    char *cmp_operand ;
    bool a_is_var ;
    bool b_is_var ;
} ;

/*[>struct switch_chain {<]*/
    /*[>int case_num ;<]*/
    /*[>switch_chain *next ;<]*/
/*[>}<]*/

struct switch_test_t {
    int switch_var;
//    switch_chain *case_chain ;     //the first case_chain member corresponding to the first succ_edges, default branch corresponding to the last succ_edges.
    int *case_chain ;
} ;

/*struct junction_t {*/
    /*bool is_simple_junction ;*/
/*} ;*/

struct call_argument {
    char *arg_name ;
    int arg_type ;
    bool is_pointer ;
    bool is_struct ;
    char *struct_name ;
//    call_argument *next ;
} ;

struct call_parameter {
    char *var_number ;
    bool is_var ;
} ;

struct call_t {
    int dst_name ;
    int func_number ;
    int parameter_num ;
    call_parameter *actual_parameter[MAX_INPUT_VAR] ;
} ;

struct token_list {
    char *token_name ;
    cfg_node_t *pointer ;
    cfg_node_t *while_pointer ;
} ;

struct return_t {
    char *return_num ;
    bool return_is_var ;
} ;

/*struct func_vars {*/
    /*char *name ;*/
    /*int variable_type ;*/
    /*int effect_domain ;*/
/*} ;*/

struct cfg_edge_t {
    int edge_id ;
    cfg_node_t *start_node ;
    cfg_node_t *end_node ;
    edge_context *context_set ;
//    cfg_edge_t *next ;
} ;


struct cfg_node_t {
    int node_id ;
    int pre_edges_num ;
    int succ_edges_num ;
    cfg_edge_t *pre_edges[MAX_EDGE_NUM] ;
    cfg_edge_t *succ_edges[MAX_EDGE_NUM] ;
    node_type_t node_type ;
    bool is_if_junction ;
    call_t *call_i ;
//    declaration_t *declaration_i ;
    assignment_t *assignment_i ;
    if_test_t *if_test_i ;
    switch_test_t *switch_test_i ;
    return_t *return_i ;
//    junction_t *junction_i ;

} ;

struct cfg_func_t {
    char *func_name ;
    int func_num ;
    int edge_num ;
    int node_num ;
    int var_num ;
//    char *return_num ;
//    bool return_is_var ;
    call_argument *input_argument[MAX_INPUT_VAR] ;
    declaration_t *func_vars_table[MAX_FUNC_VARS] ;
    cfg_edge_t *pre_entry ;
    int exist_token_num ;
    int need_token_num ;
    token_list *exist_tokens[MAX_TOKEN_NUM] ;
    token_list *need_tokens[MAX_TOKEN_NUM] ;

} ;


cfg_func_t **new_functions() ;



cfg_func_t *new_func() ;

call_argument *new_call_argument() ;

declaration_t *new_declaration() ;

assignment_t *new_assignment() ;

cfg_edge_t *new_edge(cfg_func_t *function) ;

cfg_node_t *new_node(cfg_func_t *function) ;

token_list *new_token_list() ;

if_test_t *new_if() ;

call_parameter *new_call_parameter() ;

call_t *new_call() ;

char *copy_string(char *str) ;


//estimate whether a string is a function added in the function table(return the position), or an unknown function name(return -1).
int is_known_func(char *seek, cfg_func_t **functions) ;

//is a instant number
char *is_instant_number(char *seek) ;

//get array index like a[17], return int 17
char *get_array_num(char *seek) ;

//estimate if the string is array, and return the variable position of the array as a string.
char *is_array(char *seek, cfg_func_t *function, int current_domain) ;

//find a string in the func_vars_table, return the position
char *get_var_position(char *seek, cfg_func_t *function, int current_domain) ;

void build_vars_table(char *line_buffer, cfg_func_t *function, int var_type, int effect_domain) ;

//link two nodes with a new edge.
void link_nodes(cfg_node_t *a, cfg_node_t *b, cfg_func_t *function) ;

void add_need_token(char *seek, cfg_node_t *pointer, cfg_func_t *function) ;

void add_exist_token(char *seek, cfg_func_t *function) ;

//add a junction node before the input node.
cfg_node_t *add_pre_junction(cfg_node_t *source, cfg_func_t *function) ;

//if the last exist token hasn't pointer to a node, link the need_node to the new_current_node.
void link_last_token(cfg_node_t *new_current_node, cfg_func_t *function) ;

cfg_node_t *creat_if_junction(cfg_node_t *temp_node, cfg_func_t *function) ;

//interpose a while junction between the if junction and it's succ junction.
cfg_node_t *add_while_junction(cfg_node_t *if_junc_node, cfg_func_t *function) ;

//if_test
void build_if_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) ;

cfg_node_t *make_assign_call(char *line_str, cfg_node_t *current_node, cfg_func_t *function, cfg_func_t **functions, int current_domain) ;

cfg_node_t *creat_goto_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function) ;

void creat_switch_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) ;

void creat_return_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) ;

void build_cfg_tree(FILE *fp, cfg_func_t *function, cfg_func_t **function_table) ;


void build_input_args(FILE *fp, cfg_func_t *function) ;

cfg_func_t **build_cfgs(char *cfg_file, char *glob_var_file) ;




#endif
