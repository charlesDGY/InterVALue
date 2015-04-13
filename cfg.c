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
 * $Id: cfg.c,v 1.2 2006/06/24 08:54:56 lixianfe Exp $
 *
 ******************************************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cfg.h"


#define MAX_FUNC 200

#define MAX_FUNC_NAME 60

#define MAX_TYPE_NAME 60

#define MAX_INPUT_VAR 20

#define MAX_FUNC_VARS 1024


typedef enum {DECLARATION, ASSIGNMENT, IF_TEST, SWITCH_TEST, JUNCTION, CALL, UNKNOWN_CALL} node_type_t ;

typedef struct declaration_t declaration_t ;
typedef struct assignment_t assignment_t ;
typedef struct if_test_t if_test_t ;
typedef struct switch_test_t switch_test_t ;
typedef struct junction_t junction_t ;
typedef struct call_t call_t ;
//typedef struct switch_chain switch_chain ;
typedef struct call_argument call_argument ;
//typedef struct func_vars func_vars ;

struct declaration_t {
    char *name ;
    int variable_type ;
    bool is_pointer ;
    bool is_array ;
//    bool is_struct ;        // if is struct , the type number is 13
    char *struct_name ;
    bool is_static ;
    int array_len ;
    int effect_domain ;
} ;

struct assignment_t {
    char *dst_name ;
    char *operator_a ;
    char *operator_b ;
    char *operand ;
    bool is_type_convert ;     //if is_type_convert is true, operator_a saves the type to convert, operator_b saves the src variable.
} ;

struct if_test_t {
    char *cmp_a ;
    char *cmp_b ;
    char *cmp_operand ;
} ;

/*[>struct switch_chain {<]*/
    /*[>int case_num ;<]*/
    /*[>switch_chain *next ;<]*/
/*[>}<]*/

struct switch_test_t {
    char *switch_value ;
//    switch_chain *case_chain ;     //the first case_chain member corresponding to the first succ_edges, default branch corresponding to the last succ_edges.
    int *case_chain ;
} ;

struct junction_t {
    bool is_simple_junction ;
} ;

struct call_argument {
    char *arg_name ;
    int arg_type ;
    bool is_pointer ;
    bool is_struct ;
    char *struct_name ;
//    call_argument *next ;
} ;

struct call_t {
    char *dst_name ;
    char *call_name ;
    call_argument *input_chain ;
} ;


/*struct func_vars {*/
    /*char *name ;*/
    /*int variable_type ;*/
    /*int effect_domain ;*/
/*} ;*/


typedef struct cfg_edge_t cfg_edge_t ;
typedef struct cfg_node_t cfg_node_t ;
typedef struct cfg_func_t cfg_func_t ;

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
    cfg_edge_t **pre_edges ;
    cfg_edge_t **succ_edges ;
    node_type_t node_type ;
//    declaration_t *declaration_i ;
    assignment_t *assignment_i ;
    if_test_t *if_test_i ;
    switch_test_t *switch_test_i ;
    junction_t *junction_t ;
    call_t *call_i ;

} ;

struct cfg_func_t {
    char *func_name ;
    int func_num ;
    int edge_num ;
    int node_num ;
    call_argument *input_argument[MAX_INPUT_VAR] ;
    declaration_t *func_vars_table[MAX_FUNC_VARS] ;
    cfg_edge_t *pre_entry ;
} ;


/*/////////////////////////////////////////////////////////////////////////////////////////////////*/
/*//dgy*/


char const *sys_var_type[] = {
    "int",
    "char",
    "short int",
    "long int",
    "long long int",
    "float",
    "double",
    "unsigned int",
    "unsigned char",
    "short unsigned int",
    "long unsigned int",
    "long long unsigned int",
    "unsigned",
    "struct",
    "const",
    "static",
    "extern",
    "typedef",
    NULL
} ;


cfg_func_t **new_functions() {
    cfg_func_t **p = (cfg_func_t **)malloc(MAX_FUNC * (sizeof *p)) ;
    if (p == NULL) {
        perror("new_functions out of memory!!") ;
        exit(EXIT_FAILURE) ;
    }
    return p ;
}



cfg_func_t *new_func() {
	cfg_func_t *p = (cfg_func_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new cfg_func_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->node_num = 0 ;
    p->edge_num = 0 ;
    p->input_argument[0] = NULL ;
    p->func_vars_table[0] = NULL ;
}

call_argument *new_call_argument() {
	call_argument *p = (call_argument *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new call_argument out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->arg_type = -1 ;
    p->is_pointer = false ;
    p->is_struct = false ;
    p->struct_name = NULL ;
	return p;
}


cfg_edge_t *new_edge() {
    cfg_edge_t *p = (cfg_edge_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new cfg_edge_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->start_node = NULL ;
    p->end_node = NULL ;
}
/*void free_node(interval_node *p)*/
/*{*/
	/*free(p);*/
/*}*/

declaration_t *new_declaration() {
    declaration_t *p = (declaration_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new declaration out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->array_len = -1 ;
    p->struct_name = NULL ;
    p->is_struct = false ;
    p->is_array = false ;
    p->is_pointer = false ;
    p->is_static = false ;

}


cfg_node_t *new_node() {
    cfg_node_t *p = (cfg_node_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new node out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->array_len = -1 ;
    p->struct_name = NULL ;
    p->is_struct = false ;
    p->is_array = false ;
    p->is_pointer = false ;
    p->is_static = false ;


}
char *copy_string(char *str) {
    char *result = NULL ;
    result = strdup(str) ;
    if (result == NULL) {
        perror("copy string error!!") ;
        exit(EXIT_FAILURE) ;
    }
    return result ;
}


void build_func_table(FILE *fp, cfg_func_t *function, char *var_type_buffer, int var_type, int effect_domain, int var_num) {
    //read declaration and store
    int row = 0, type_token = 0 ;
    char type_buffer[10][MAX_TYPE_NAME] ;    //the longest input argument is "static const long long unsigned int * name = 4B;". so the row is 10.
    int i, var_num = 0 ;
    int start, end, length ;
    char const **sys_type = NULL ;
    char const_var[] = "const" ;
    char struct_var[] = "struct" ;
    char point_c[] = "*" ;
    char *temp = NULL ;


    if(var_type != 17) {
        ch = fgetc(fp) ;
        while ((ch = fgetc(fp)) != ';') {
            if (ch == ' ') {
                type_buffer[row][type_token] = '\0' ;
                row++ ;
                type_token = 0 ;
            }
            else {
                type_buffer[row][type_token] = ch ;
                type_token++ ;
            }
        }
        type_buffer[row][type_token] = '\0' ;
        function->func_vars_table[var_num] = new_declaration() ;
        if (var_type == 15) {

        }
        if (var_type != 16 || var_type == 14) {

        }





        if (strcmp(type_buffer[0], const_var) == 0) {
            if (strcmp(type_buffer[1], struct_var) == 0) {
                function->input_argument[arg_num]->is_struct = true ;
                function->input_argument[arg_num]->struct_name = copy_string(type_buffer[2]) ;
                start = 3 ;
            }
            else {
                start = 1 ;
            }
        }
        else if (strcmp(type_buffer[0], struct_var) == 0) {
            function->input_argument[arg_num]->is_struct = true ;
            function->input_argument[arg_num]->struct_name = copy_string(type_buffer[1]) ;
            start = 2 ;
        }
        else {
            start = 0 ;
        }
        //set the is_pointer bool member
        if (strcmp(type_buffer[row-1], point_c) == 0) {
            function->input_argument[arg_num]->is_pointer = true ;
            end = row - 1 ;
        }
        else {
            end = row ;
        }
        //store the arg name
        function->input_argument[arg_num]->arg_name = copy_string(type_buffer[row]) ;
        //set the variable type number
        var_type_buffer[0] = '\0' ;
        for (i = start; i < end; i++) {
            if (i != end - 1) {
                length = strlen(type_buffer[i]) ;
                type_buffer[i][length] = ' ' ;
                type_buffer[i][length + 1] = '\0' ;
            }
            temp = strcat(var_type_buffer, type_buffer[i]) ;
        }
        if (var_type_buffer[0] != '\0') {
            for(sys_type = sys_var_type; *sys_type != NULL; sys_type++) {
                if (strcmp(var_type_buffer, *sys_type) == 0) {
                    function->input_argument[arg_num]->arg_type = sys_type - sys_var_type ;
                }
            }
        }
        //set control variable
        row = 0 ;
        type_token = 0 ;
        arg_num++ ;
        if (ch == ',') {
            ch = fgetc(fp) ;
        }

        fgets(var_type_buffer, MAX_TYPE_NAME, fp);
    }
}


void build_cfg_tree(FILE *fp, cfg_func_t *function, cfg_func_t **function_table) {
    //start
    int ch ;
    //first string buffer
    char var_type_buffer[MAX_TYPE_NAME] ;

    //effect_domain
    int range_stack[MAX_RANGE_DEPTH], range_top = 1 ;
    range_buffer[0] = 0 ;
    int range_num = 0 ;
    int current_domain = 0 ;

    //has try {} and finally{}
    unsigned char has_try = 0 ;
    //compared string
    char try_var[] = "try" ;
    char left_bracket[] = "{" ;
    char right_bracket[] = "}" ;
    char if_test_s[] = "if" ;
    char switch_test_s[] = "switch" ;

    //estimate whether is sys_type to define whether is declaration
    int var_type = -1 ;
    char const **sys_type = NULL ;

    //the number of vars of the function;
    int var_num = 0 ;


    while (range_buffer[top-1] != 0) {
        //read first string
        fscanf(fp,"%s", var_type_buffer) ;
        //if is "{"
        if (strcmp(var_type_buffer, left_bracket) == 0) {
            if (has_try == 0) {
                range_num++ ;
                range_stack[top++] = range_num ;
                current_domain = range_num ;
            }
            else {
                range_stack[top] = range_stack[top-1] ;
                top++ ;
            }
            has_try = 0 ;
        }
        //&& \n !!enum !!else
        if (strcmp(var_type_buffer, try_var) == 0) {
            has_try = 1 ;
        }
        if (strcmp(var_type_buffer, finally_var) == 0) {
            while (strcmp(var_type_buffer, right_bracket) != 0) {
                fscanf(fp,"%s", var_type_buffer) ;
            }
        }
        if (strcmp(var_type_buffer, right_bracket) == 0) {
            top-- ;
            current_domain = range_stack[top-1] ;
        }
        //if_test
        if (strcmp(var_type_buffer, if_test_s)) {
            fscanf(fp," (%s %s %s %*s %s %*s %*s %s", var_type_buffer) ;
        }

        //switch_test
        if (strcmp(var_type_buffer, switch_test_s) == 0) {
            fscanf(fp," (%s <default: %s")
        }

        //junction_t
        if (var_type_buffer[0] == '<') {

        }


        //declaration_t and assignment_t and call_t

        for(sys_type = sys_var_type; *sys_type != NULL; sys_type++) {
            if (strcmp(var_type_buffer, *sys_type) == 0) {
                var_type = sys_type - sys_var_type ;
            }
        }

        //declaration_t, except enum
        if (var_type != -1) {
            build_func_table(fp, function, var_type, current_domain, var_num) ;
            var_num ++ ;
        }
    }
    else {

    }


}


void build_input_args(FILE *fp, cfg_func_t *function) {
    char var_type_buffer[MAX_TYPE_NAME] ;
    //get function input arg_nameument
    int ch ;
    int row = 0, type_token = 0 ;
    char type_buffer[7][MAX_TYPE_NAME] ;    //the longest input argument is "const long long unsigned int * name". so the row is 7.
    int i, arg_num = 0 ;
    int start, end, length ;
    char const **sys_type = NULL ;
    char const_var[] = "const" ;
    char struct_var[] = "struct" ;
    char point_c[] = "*" ;
    char *temp = NULL ;

    ch = fgetc(fp) ;
    ch = fgetc(fp) ;

    while ((ch = fgetc(fp)) != '\n') {
        if (ch == ',' || ch == ')') {
            if (row == 0 && type_token == 0) {
                continue ;
            }
            type_buffer[row][type_token] = '\0' ;
            function->input_argument[arg_num] = new_call_argument() ;
            if (strcmp(type_buffer[0], const_var) == 0) {
                if (strcmp(type_buffer[1], struct_var) == 0) {
                    function->input_argument[arg_num]->is_struct = true ;
                    function->input_argument[arg_num]->struct_name = copy_string(type_buffer[2]) ;
                    start = 3 ;
                }
                else {
                    start = 1 ;
                }
            }
            else if (strcmp(type_buffer[0], struct_var) == 0) {
                function->input_argument[arg_num]->is_struct = true ;
                function->input_argument[arg_num]->struct_name = copy_string(type_buffer[1]) ;
                start = 2 ;
            }
            else {
                start = 0 ;
            }
            //set the is_pointer bool member
            if (strcmp(type_buffer[row-1], point_c) == 0) {
                function->input_argument[arg_num]->is_pointer = true ;
                end = row - 1 ;
            }
            else {
                end = row ;
            }
            //store the arg name
            function->input_argument[arg_num]->arg_name = copy_string(type_buffer[row]) ;
            //set the variable type number
            var_type_buffer[0] = '\0' ;
            for (i = start; i < end; i++) {
                if (i != end - 1) {
                    length = strlen(type_buffer[i]) ;
                    type_buffer[i][length] = ' ' ;
                    type_buffer[i][length + 1] = '\0' ;
                }
                temp = strcat(var_type_buffer, type_buffer[i]) ;
            }
            if (var_type_buffer[0] != '\0') {
                for(sys_type = sys_var_type; *sys_type != NULL; sys_type++) {
                    if (strcmp(var_type_buffer, *sys_type) == 0) {
                        function->input_argument[arg_num]->arg_type = sys_type - sys_var_type ;
                    }
                }
            }
            //set control variable
            row = 0 ;
            type_token = 0 ;
            arg_num++ ;
            if (ch == ',') {
                ch = fgetc(fp) ;
            }
        }
        else if (ch == ' ') {
            type_buffer[row][type_token] = '\0' ;
            row++ ;
            type_token = 0 ;
        }
        else {
            type_buffer[row][type_token] = ch ;
            type_token++ ;
        }
    }

    //set the token of input_argument tail
    function->input_argument[arg_num] = NULL ;






//    fscanf(fp," (%s", var_type_buffer) ;

    //
}


cfg_func_t **build_cfgs(char *cfg_file, char *glob_var_file) {
    FILE *fp ;
    fp = fopen(cfg_file, "r") ;
    if (fp == NULL) {
        perror("file open error!!!") ;
        exit(EXIT_FAILURE) ;
    }

    char func_name_buffer[MAX_FUNC_NAME] ;
    char row_buffer[MAX_ROW_LENGTH] ;
    char *func_name ;
    cfg_func_t **result_cfgs = NULL ;
    cfg_func_t **functions = new_functions() ;
    int func_num = 0 ;
    int ch ;

    fseek(fp, 0, SEEK_SET);
    //generate function_table
    while ((ch = fgetc(fp)) != EOF) {
        if (ch != ' ' && ch != '{' && ch != '}') {
            ungetc(ch, fp) ;
            functions[func_num] = new_func() ;
            //get function name
            fscanf(fp,"%s", func_name_buffer) ;
            func_name = copy_string(func_name_buffer) ;
            functions[func_num]->func_name = func_name ;
            functions[func_num]->func_num = func_num ;
            func_num++ ;
        }
        fgets(row_buffer, MAX_ROW_LENGTH, fp);
    }
    functions[func_num] = NULL ;

    fseek(fp, 0, SEEK_SET);

    for (func_num = 0; functions[func_num] != NULL; func_num++) {
        fscanf(fp,"%s", func_name_buffer) ;
        //store input arguments
        build_input_args(fp, functions[func_num]) ;
        //build_function cfg_tree
        build_cfg_tree(fp, functions[func_num], functions) ;

        while ((ch = fgetc(fp)) == '\n') ;
        ungetc(ch, fp) ;
    }



    fclose(fp) ;

    result_cfgs = functions ;
    return result_cfgs ;
}



/*char *readword()*/

    /*// locate the text section*/
    /*fseek(fp, 0, SEEK_SET);*/
    /*fread(&fhdr, sizeof(fhdr), 1, fp);*/
    /*fread(&ahdr, sizeof(ahdr), 1, fp);*/
    /*for (i=0; i<fhdr.f_nscns; i++) {*/
	/*fread(&shdr, sizeof(shdr), 1, fp);*/
	/*if (shdr.s_flags != ECOFF_STYP_TEXT)*/
		/*continue;*/
	/*text_size = shdr.s_size;*/
	/*text_offset = shdr.s_scnptr;*/
	/*text_entry = shdr.s_vaddr;*/


