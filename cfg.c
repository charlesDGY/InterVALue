/******************************************************************************
 *
 *       COPYRIGHT NOTICE
 *       Copyright (c) 2015
 *       All rights reserved
 *
 *       @author       :  Gaoyang Dai
 *       @email        :  edward.d.erlic@gmail.com
 *       @file         :  /home/dgy/Programming/VInterval/cfg.c
 *       @date         :  2015/04/14 14:27
 *       @description  :
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cfg.h"


/*#define MAX_FUNC_NUM 100*/

/*#define MAX_FUNC_NAME 60*/

/*#define MAX_TYPE_NAME 60*/

/*#define MAX_INPUT_VAR 20*/

/*#define MAX_FUNC_VARS 1024*/

/*#define MAX_RANGE_DEPTH 20*/

/*#define MAX_LINE_LENGTH 1024*/

/*#define MAX_TOKEN_NUM 1024*/

/*#define MAX_EDGE_NUM 64*/

/*typedef enum {ENTRY, RETURN, GOTO, DECLARATION, ASSIGNMENT, IF_TEST, SWITCH_TEST, JUNCTION, CALL, UNKNOWN_CALL} node_type_t ;*/

/*typedef struct declaration_t declaration_t ;*/
/*typedef struct assignment_t assignment_t ;*/
/*typedef struct if_test_t if_test_t ;*/
/*typedef struct switch_test_t switch_test_t ;*/
/*//typedef struct junction_t junction_t ;*/
/*typedef struct call_t call_t ;*/
/*//typedef struct switch_chain switch_chain ;*/
/*typedef struct call_argument call_argument ;*/
/*typedef struct call_parameter call_parameter ;*/
/*typedef struct token_list token_list ;*/
/*//typedef struct func_vars func_vars ;*/

/*struct declaration_t {*/
    /*char *name ;*/
    /*int variable_type ;*/
    /*bool is_pointer ;*/
    /*bool is_array ;*/
    /*bool is_struct ;        // if is struct , the type number is 13*/
    /*char *struct_name ;*/
    /*bool is_static ;*/
    /*int array_len ;*/
    /*int effect_domain ;*/
/*} ;*/

/*struct assignment_t {*/
    /*int *dst_name ;*/
    /*char *operator_a ;*/
    /*char *operator_b ;*/
    /*char *operand ;*/
    /*bool is_type_convert ;     //if is_type_convert is true, operator_a saves the type to convert, operator_b saves the src variable.*/
    /*bool a_is_var ;*/
    /*bool b_is_var ;*/
    /*int has_array ;            //if dst is array, has_array == 1, if a is array, has_array == 2, if no array, has_array == 0.*/
    /*char *array_offset ;       //there will be at most one array within an assignment.*/
    /*bool offset_is_var ;*/
/*} ;*/

/*struct if_test_t {*/
    /*char *cmp_a ;*/
    /*char *cmp_b ;*/
    /*char *cmp_operand ;*/
    /*bool a_is_var ;*/
    /*bool b_is_var ;*/
/*} ;*/

/*[>[>struct switch_chain {<]<]*/
    /*[>[>int case_num ;<]<]*/
    /*[>[>switch_chain *next ;<]<]*/
/*[>[>}<]<]*/

/*struct switch_test_t {*/
    /*int switch_var;*/
/*//    switch_chain *case_chain ;     //the first case_chain member corresponding to the first succ_edges, default branch corresponding to the last succ_edges.*/
    /*int *case_chain ;*/
/*} ;*/

/*[>struct junction_t {<]*/
    /*[>bool is_simple_junction ;<]*/
/*[>} ;<]*/

/*struct call_argument {*/
    /*char *arg_name ;*/
    /*int arg_type ;*/
    /*bool is_pointer ;*/
    /*bool is_struct ;*/
    /*char *struct_name ;*/
/*//    call_argument *next ;*/
/*} ;*/

/*struct call_parameter {*/
    /*char *var_number ;*/
    /*bool is_var ;*/
/*} ;*/

/*struct call_t {*/
    /*char *dst_name ;*/
    /*int func_number ;*/
    /*int parameter_num ;*/
    /*call_parameter *actual_parameter[MAX_INPUT_VAR] ;*/
/*} ;*/

/*struct token_list {*/
    /*char *token_name ;*/
    /*cfg_node_t *pointer ;*/
    /*cfg_node_t *while_pointer ;*/
/*} ;*/


/*[>struct func_vars {<]*/
    /*[>char *name ;<]*/
    /*[>int variable_type ;<]*/
    /*[>int effect_domain ;<]*/
/*[>} ;<]*/


/*typedef struct cfg_edge_t cfg_edge_t ;*/
/*typedef struct cfg_node_t cfg_node_t ;*/
/*typedef struct cfg_func_t cfg_func_t ;*/

/*struct cfg_edge_t {*/
    /*int edge_id ;*/
    /*cfg_node_t *start_node ;*/
    /*cfg_node_t *end_node ;*/
    /*edge_context *context_set ;*/
/*//    cfg_edge_t *next ;*/
/*} ;*/


/*struct cfg_node_t {*/
    /*int node_id ;*/
    /*int pre_edges_num ;*/
    /*int succ_edges_num ;*/
    /*cfg_edge_t *pre_edges[MAX_EDGE_NUM] ;*/
    /*cfg_edge_t *succ_edges[MAX_EDGE_NUM] ;*/
    /*node_type_t node_type ;*/
    /*bool is_if_junction ;*/
    /*call_t *call_i ;*/
/*//    declaration_t *declaration_i ;*/
    /*assignment_t *assignment_i ;*/
    /*if_test_t *if_test_i ;*/
    /*switch_test_t *switch_test_i ;*/
/*//    junction_t *junction_i ;*/

    /*call_t *call_i ;*/

/*} ;*/

/*struct cfg_func_t {*/
    /*char *func_name ;*/
    /*int func_num ;*/
    /*int edge_num ;*/
    /*int node_num ;*/
    /*int var_num ;*/
    /*char *return_num ;*/
    /*bool return_is_var ;*/
    /*call_argument *input_argument[MAX_INPUT_VAR] ;*/
    /*declaration_t *func_vars_table[MAX_FUNC_VARS] ;*/
    /*cfg_edge_t *pre_entry ;*/
    /*int exist_token_num ;*/
    /*int need_token_num ;*/
    /*token_list *exist_tokens[MAX_TOKEN_NUM] ;*/
    /*token_list *need_tokens[MAX_TOKEN_NUM] ;*/

/*} ;*/


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
//    "extern",
    "typedef",
    "long",
    "short",
    "extern",
    NULL
} ;

//assume that all edge_context is originally generated to the same length and same variable sort.
edge_context *union_context(edge_context *head_a, edge_context *head_b, cfg_func_t *function) {
    if (head_a == NULL || head_b == NULL) {
        perror("union_context's input head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    //handle null and XN condition.
    if (head_a->next == NULL) {
        return copy_context(head_b) ;
    }
    if (head_b->next == NULL) {
        return copy_context(head_a) ;
    }

    edge_context *iter_a = NULL, *iter_b = NULL ;
    edge_context *context_p = NULL, *iter_r = NULL, *result = NULL ;
    iter_a = head_a->next ;
    iter_b = head_b->next ;

    //union set and set
    while (iter_a != NULL) {
        iter_r = make_context() ;
        iter_r->name_d = iter_a->name_d ;
        iter_r->value_set = set_set_union(iter_a->value_set, iter_b->value_set, function->func_vars_table[iter_r->name_d]->variable_type) ;
        if (result == NULL) {
            result = make_context() ;
            result->next = iter_r ;
            context_p = result->next ;
        }
        else {
            context_p->next = iter_r ;
            context_p = context_p->next ;
        }
        iter_a = iter_a->next ;
        iter_b = iter_b->next ;
    }
    return result ;

}

edge_context *union_context_new(edge_context *head_a, edge_context *head_b, int type_array[]) {
    if (head_a == NULL || head_b == NULL) {
        perror("union_context's input head is NULL!") ;
        exit(EXIT_FAILURE) ;
    }
    //handle null and XN condition.
    if (head_a->next == NULL) {
        return copy_context(head_b) ;
    }
    if (head_b->next == NULL) {
        return copy_context(head_a) ;
    }

    edge_context *iter_a = NULL, *iter_b = NULL ;
    edge_context *context_p = NULL, *iter_r = NULL, *result = NULL ;
    iter_a = head_a->next ;
    iter_b = head_b->next ;

    //union set and set
    while (iter_a != NULL) {
        iter_r = make_context() ;
        iter_r->name_d = iter_a->name_d ;
        iter_r->value_set = set_set_union(iter_a->value_set, iter_b->value_set, type_array[iter_r->name_d]) ;
        if (result == NULL) {
            result = make_context() ;
            result->next = iter_r ;
            context_p = result->next ;
        }
        else {
            context_p->next = iter_r ;
            context_p = context_p->next ;
        }
        iter_a = iter_a->next ;
        iter_b = iter_b->next ;
    }
    return result ;

}




cfg_func_t **new_functions() {
    cfg_func_t **p = (cfg_func_t **)malloc(MAX_FUNC_NUM * (sizeof *p)) ;
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
    p->func_name = NULL ;
    p->node_num = 0 ;
    p->edge_num = 0 ;
    //the number of vars of the function;
    p->var_num = 0 ;
//    p->return_is_var = false ;
//    p->return_num = NULL ;
    p->input_argument[0] = NULL ;
    p->func_vars_table[0] = NULL ;
    //token
    p->exist_token_num = 0 ;
    p->need_token_num = 0 ;
    p->exist_tokens[0] = NULL ;
    p->need_tokens[0] = NULL ;
    p->pre_entry = NULL ;

    p->all_edges[0] = NULL ;
    p->all_nodes[0] = NULL ;

    return p ;
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

    return p ;
}

assignment_t *new_assignment() {
    assignment_t *p = (assignment_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new declaration out of memory!") ;
        exit(EXIT_FAILURE) ;
    }

    p->operator_a = NULL ;
    p->operator_b = NULL ;
    p->operand = NULL ;
    p->is_type_convert = false ;
    p->a_is_var = false ;
    p->b_is_var = false ;
    p->has_array = 0 ;            //if dst is array, has_array == 1, if a is array, has_array == 2, if no array, has_array == 0.
    p->array_offset = NULL ;       //there will be at most one array within an assignment.
    p->offset_is_var = false ;

    return p ;
}


cfg_edge_t *new_edge(cfg_func_t *function) {
    cfg_edge_t *p = (cfg_edge_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new cfg_edge_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->start_node = NULL ;
    p->end_node = NULL ;
    p->context_set = NULL ;
    p->edge_id = function->edge_num ;

    function->all_edges[function->edge_num] = p ;
    function->edge_num++ ;
    function->all_edges[function->edge_num] = NULL ;

    return p ;
}

cfg_node_t *new_node(cfg_func_t *function) {
    cfg_node_t *p = (cfg_node_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new node out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->pre_edges_num = 0 ;
    p->succ_edges_num = 0 ;
    p->pre_edges[0] = NULL ;
    p->succ_edges[0] = NULL ;
    //node_type ;
    //declaration_t *declaration_i ;
    p->assignment_i = NULL ;
    p->if_test_i = NULL ;
    p->switch_test_i = NULL ;
    p->return_i = NULL ;
    //p->junction_t = NULL ;
    p->is_if_junction = false ;
    p->node_id = function->node_num ;

    function->all_nodes[function->node_num] = p ;
    function->node_num++ ;
    function->all_nodes[function->node_num] = NULL ;


    return p ;
}

token_list *new_token_list() {
    token_list *p = (token_list *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new token_list out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->token_name = NULL ;
    p->pointer = NULL ;
    p->while_pointer = NULL ;

    return p ;
}

if_test_t *new_if() {
    if_test_t *p = (if_test_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new if_test_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->cmp_a = NULL ;
    p->cmp_b = NULL ;
    p->cmp_operand = NULL ;
    p->a_is_var = false ;
    p->b_is_var = false ;

    return p ;
}

case_t *new_case() {
    case_t *p = (case_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new case is out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->case_number = 0 ;
    p->token_name = NULL ;
    return p ;
}

switch_test_t *new_switch() {
    switch_test_t *p = (switch_test_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new switch_test_t is out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->switch_var = -1 ;
    p->case_chain[0] = NULL ;
    p->case_num = 0 ;

    return p ;
}



call_parameter *new_call_parameter() {
    call_parameter *p = (call_parameter *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new call_parameter out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->var_number = NULL ;
    p->is_var = false ;

    return p ;
}

call_t *new_call() {
    call_t *p = (call_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new call_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->dst_name = -1 ;
    //p->func_number = 0 ;
    p->parameter_num = 0 ;
    p->actual_parameter[0] = NULL ;

    return p ;
}

return_t *new_return() {
    return_t *p = (return_t *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("new return_t out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->return_num = NULL ;
    p->return_is_var = false ;
    return p ;
}


char *copy_string(char *str) {
    char *result = NULL ;
    if (str != NULL) {
        result = strdup(str) ;
    }
    return result ;
}

//estimate whether a string is a function added in the function table(return the position), or an unknown function name(return -1).
int is_known_func(char *seek, cfg_func_t **functions) {
    cfg_func_t **pointer = NULL ;
    int temp = -1 ;
    for (pointer = functions; *pointer != NULL; pointer++) {
        if (strcmp((*pointer)->func_name, seek) == 0) {
            temp = pointer - functions ;
            break ;
        }
    }
    return temp ;
}

char *remove_dot(char *src) {
    //judge whether is the same variable like int j.1 and int j.2
    char *array_token = NULL ;
    char *result = NULL ;
    result = copy_string(src) ;
    array_token = strchr(result, '.') ;
    if (array_token != NULL && !(result[0] == 'D' && result[1] == '.' && result[2] >= '0' && result[2] <= '9')) {
        array_token = '\0' ;
    }

    return result ;
}

//is a instant number
char *is_instant_number(char *seek) {
    char *pointer = NULL ;
    pointer = seek ;
    if ((*pointer >= '0' && *pointer <= '9') || (*pointer == '-' && *(pointer + 1) >= '0' && *(pointer + 1) <= '9')) {
        pointer = copy_string(seek) ;
    }
    else {
        pointer = NULL ;
    }
    return pointer ;
}

//get array index like a[17], return int 17
char *get_array_num(char *seek) {
    char var_type_buffer[MAX_TYPE_NAME] ;
    char *array_token = NULL ;
    char *pointer = NULL ;
    int i = 0 ;
    pointer = seek ;
    array_token = strchr(pointer, '[') ;
    if (array_token == NULL) {
        perror("the string is not an array!!!") ;
        exit(EXIT_FAILURE) ;
    }
    array_token++ ;
    while (*array_token != ']') {
        var_type_buffer[i] = *array_token ;
        i++ ;
        array_token++ ;
    }
    var_type_buffer[i] = '\0' ;
    pointer = copy_string(var_type_buffer) ;
    return pointer ;
}

//estimate if the string is array, and return the variable position of the array as a string.
char *is_array(char *seek, cfg_func_t *function, int current_domain) {
    char var_type_buffer[MAX_TYPE_NAME] ;
    declaration_t **var_table = NULL ;
    char *pointer = NULL ;
    int temp_var = -1 ;
    char *array_token = NULL ;
    int temp_domain = 0 ;

    pointer = seek ;
    array_token = strchr(pointer, '[') ;
    if (array_token != NULL && pointer[strlen(pointer) - 1] == ']') {
        *array_token = '\0' ;
        for (var_table = function->func_vars_table; *var_table != NULL; var_table++) {
            if (strcmp((*var_table)->name, pointer) == 0 && (*var_table)->effect_domain <= current_domain) {
                if ((*var_table)->effect_domain > temp_domain) {
                    temp_var = var_table - function->func_vars_table ;
                    temp_domain = (*var_table)->effect_domain ;
                }
            }
        }
        if (temp_var == -1) {
            pointer = NULL ;
        }
        else {
            sprintf(var_type_buffer, "%d", temp_var) ;
            pointer = copy_string(var_type_buffer) ;
        }
        *array_token = '[' ;
    }
    else {
        pointer = NULL ;
    }
    return pointer ;
}
//find a string in the func_vars_table, return the position
char *get_var_position(char *seek, cfg_func_t *function, int current_domain) {
    char var_type_buffer[MAX_TYPE_NAME] ;
    declaration_t **var_table = NULL ;
    char *pointer = NULL ;
    int temp_var = -1 ;
    char *array_token = NULL ;
    char struct_pointer[] = "->" ;
    int is_struct = 0 ;
    int temp_domain = -1 ;

    pointer = copy_string(seek) ;
    array_token = strchr(pointer, '.') ;
    if (array_token != NULL && !(pointer[0] == 'D' && pointer[1] == '.' && pointer[2] >= '0' && pointer[2] <= '9')) {
        if (*(array_token + 1) >= '0' && *(array_token + 1) <= '9') {
            *array_token = '\0' ;
        }
        else {
            is_struct = 1 ;
        }
    }
    else {
        array_token = strstr(pointer, struct_pointer) ;
        if (array_token != NULL) {
            is_struct = 2 ;
        }
    }

    for (var_table = function->func_vars_table; *var_table != NULL; var_table++) {
        if (strcmp((*var_table)->name, pointer) == 0 && (*var_table)->effect_domain <= current_domain) {
            if ((*var_table)->effect_domain > temp_domain) {
                temp_var = var_table - function->func_vars_table ;
                temp_domain = (*var_table)->effect_domain ;
            }
        }
    }
    if (temp_var == -1) {
        if (is_struct == 1 || is_struct == 2) {
            *array_token = '\0' ;
            for (var_table = function->func_vars_table; *var_table != NULL; var_table++) {
                if (strcmp((*var_table)->name, pointer) == 0 && (*var_table)->effect_domain <= current_domain &&
                        (*var_table)->is_struct == true) {
                    if ((*var_table)->effect_domain > temp_domain) {
                        temp_var = var_table - function->func_vars_table ;
                        temp_domain = (*var_table)->effect_domain ;
                    }
                }
            }
            if (temp_var == -1) {
                free(pointer) ;
                pointer = NULL ;
            }
            else {
                if (is_struct == 1) {
                    *array_token = '.' ;
                }
                else {
                    *array_token = '-' ;
                }
                function->func_vars_table[function->var_num] = new_declaration() ;
                function->func_vars_table[function->var_num]->effect_domain = temp_domain ;
                function->func_vars_table[function->var_num]->name = copy_string(pointer) ;
                function->func_vars_table[function->var_num]->variable_type = 19 ;
                sprintf(var_type_buffer, "%d", function->var_num) ;
                free(pointer) ;
                pointer = copy_string(var_type_buffer) ;
                function->var_num++ ;
                function->func_vars_table[function->var_num] = NULL ;
            }
        }
        else {
            free(pointer) ;
            pointer = NULL ;
        }
    }
    else {
        free(pointer) ;
        sprintf(var_type_buffer, "%d", temp_var) ;
        pointer = copy_string(var_type_buffer) ;
    }

    return pointer ;
}

void build_vars_table(char *line_buffer, cfg_func_t *function, int var_type, int effect_domain) {
    //read declaration and store
    char var_type_buffer[MAX_TYPE_NAME] ;
    int row = 0, type_token = 0 ;
    char *type_buffer[10] ;    //the longest input argument is "static const long long unsigned int * name = 4B;". so the row is 10.
    int i ;
    int start, end, length ;
    char const **sys_type = NULL ;
    declaration_t **var_table = NULL ;
    char const_var[] = "const" ;
    char struct_var[] = "struct" ;
    char point_c[] = "*" ;
    char equal_c[] = "=" ;
    char *temp = NULL ;
    char *array_token ;
    char array_name[MAX_TYPE_NAME] ;
    int var_num = function->var_num ;
    line_buffer[strlen(line_buffer) - 1] = '\0' ;

    if(var_type != 16 && var_type != 15 && var_type != 19) {
        /*ch = fgetc(fp) ;*/
        /*row = 1 ;*/
        /*strcpy(type_buffer[0], sys_var_type[var_type]) ;*/
        /*while ((ch = fgetc(fp)) != ';') {*/
            /*if (ch == ' ') {*/
                /*type_buffer[row][type_token] = '\0' ;*/
                /*row++ ;*/
                /*type_token = 0 ;*/
            /*}*/
            /*else {*/
                /*type_buffer[row][type_token] = ch ;*/
                /*type_token++ ;*/
            /*}*/
        /*}*/
        /*type_buffer[row][type_token] = '\0' ;*/
        type_buffer[row] = strtok(line_buffer, " ") ;
        while (type_buffer[row] != NULL) {
            row++ ;
            type_buffer[row] = strtok(NULL, " ") ;
        }
        row-- ;
        //judge whether is the same variable like int j.1 and int j.2
        array_token = strchr(type_buffer[row], '.') ;
        if (array_token != NULL && !(type_buffer[row][0] == 'D' && type_buffer[row][1] == '.' && type_buffer[row][2] >= '0' && type_buffer[row][2] <= '9')) {
            temp = strncpy(array_name, type_buffer[row], array_token - type_buffer[row]) ;
            array_name[array_token - type_buffer[row]] = '\0' ;
            for(var_table = function->func_vars_table; *var_table != NULL; var_table++) {
                //handle global like int glob1.0 = glob1 ;
                if (*(array_token + 1) == '0' && strcmp(array_name, (*var_table)->name) == 0 && (*var_table)->effect_domain == 0) {
                    return ;
                }
                //handle repeat like int i.1, i.2, i.3
                if (strcmp(array_name, (*var_table)->name) == 0 && effect_domain == (*var_table)->effect_domain) {
                    return ;
                }
            }
            temp = strcpy(type_buffer[row], array_name) ;
        }

        function->func_vars_table[var_num] = new_declaration() ;
        function->func_vars_table[var_num]->effect_domain = effect_domain ;
        //store the var name
        array_token = strchr(type_buffer[row], '[') ;
        if (array_token != NULL) {
            temp = strncpy(array_name, type_buffer[row], array_token - type_buffer[row]) ;
            array_name[array_token - type_buffer[row]] = '\0' ;
            function->func_vars_table[var_num]->is_array = true ;
            function->func_vars_table[var_num]->name = copy_string(array_name) ;
            array_token++ ;
            type_buffer[row][type_token - 1] = '\0' ;
            function->func_vars_table[var_num]->array_len = atoi(array_token) ;
        }
        else {
            function->func_vars_table[var_num]->name = copy_string(type_buffer[row]) ;
        }
        //static type can't define as array.
        if (var_type == 14) {
            if (strcmp(type_buffer[1], struct_var) == 0) {
                function->func_vars_table[var_num]->is_struct = true ;
                function->func_vars_table[var_num]->struct_name = copy_string(type_buffer[2]) ;
                start = 3 ;
            }
            else {
                start = 1 ;
            }
        }
        else if (var_type == 13) {
            function->func_vars_table[var_num]->is_struct = true ;
            function->func_vars_table[var_num]->struct_name = copy_string(type_buffer[1]) ;
            start = 2 ;
        }
        else {
            start = 0 ;
        }
        //set the is_pointer bool member
        if (strcmp(type_buffer[row-1], point_c) == 0) {
            function->func_vars_table[var_num]->is_pointer = true ;
            end = row - 1 ;
        }
        else {
            end = row ;
        }
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
                    function->func_vars_table[var_num]->variable_type = sys_type - sys_var_type ;
                }
            }
        }
    }
    //static
    else if (var_type == 15) {
        if (var_type == 15) {
            //set start token
            if (strcmp(type_buffer[1], const_var) == 0) {
                start = 2 ;
            }
            else {
                start = 1 ;
            }
            //set close token
            if (strcmp(type_buffer[row - 1], equal_c) == 0) {
                if (strcmp(type_buffer[row - 3], point_c) == 0) {
                    end = row - 3 ;
                }
                else {
                    end = row - 2 ;
                }
            }
            else {
                if (strcmp(type_buffer[row - 1], point_c) == 0) {
                    end = row - 1 ;
                }
                else {
                    end = row ;
                }
            }
            //assignment !!! new node
            //
            //////////////////////////
        }
    }
    else if (var_type == 19 || var_type == 16) {
        return ;
    }
    //enum
    else {
        //fgets(var_type_buffer, MAX_TYPE_NAME, fp);
    }

    if (function->func_vars_table[function->var_num] != NULL) {
        function->var_num++ ;
        function->func_vars_table[function->var_num] = NULL ;
    }
}

//link two nodes with a new edge.
void link_nodes(cfg_node_t *a, cfg_node_t *b, cfg_func_t *function) {
    if (a == NULL || b == NULL) {
        perror("link node error, has NULL node!!") ;
        exit(EXIT_FAILURE) ;
    }
    cfg_edge_t *new_link_edge = NULL ;
    new_link_edge = new_edge(function) ;
    new_link_edge->start_node = a ;
    new_link_edge->end_node = b ;
    if (a->succ_edges_num == 2 && a->node_type == IF_TEST) {
        a->succ_edges[0] = new_link_edge ;
        a->succ_edges_num = 2;
        a->succ_edges[a->succ_edges_num] = NULL ;
        b->pre_edges[b->pre_edges_num] = new_link_edge ;
        b->pre_edges_num++ ;
        b->pre_edges[b->pre_edges_num] = NULL ;

    }
    else {
        a->succ_edges[a->succ_edges_num] = new_link_edge ;
        a->succ_edges_num++ ;
        a->succ_edges[a->succ_edges_num] = NULL ;
        b->pre_edges[b->pre_edges_num] = new_link_edge ;
        b->pre_edges_num++ ;
        b->pre_edges[b->pre_edges_num] = NULL ;

    }
}

void add_need_token(char *seek, cfg_node_t *pointer, cfg_func_t *function) {
    token_list *p = (token_list *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("add need token out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->token_name = copy_string(seek) ;
    p->pointer = pointer ;
    function->need_tokens[function->need_token_num] = p ;
    function->need_token_num++ ;
    function->need_tokens[function->need_token_num] = NULL ;
}

void add_exist_token(char *seek, cfg_func_t *function) {
    token_list *p = (token_list *)malloc(sizeof *p) ;
    if (p == NULL) {
        perror("add exist token out of memory!") ;
        exit(EXIT_FAILURE) ;
    }
    p->token_name = copy_string(seek) ;
    p->pointer = NULL ;
    function->exist_tokens[function->exist_token_num] = p ;
    function->exist_token_num++ ;
    function->exist_tokens[function->exist_token_num] = NULL ;
}

//add a junction node before the input node.
cfg_node_t *add_pre_junction(cfg_node_t *source, cfg_func_t *function) {
    cfg_node_t *junction_node = NULL ;
    cfg_edge_t *junction_edge = NULL ;
    junction_node = new_node(function) ;
    junction_edge = new_edge(function) ;
    cfg_edge_t **source_pre_edges = NULL ;
    for(source_pre_edges = source->pre_edges; *source_pre_edges != NULL; source_pre_edges++) {
        (*source_pre_edges)->end_node = junction_node ;
        junction_node->pre_edges[junction_node->pre_edges_num] = *source_pre_edges ;
        junction_node->pre_edges_num++ ;
    }
    junction_node->pre_edges[junction_node->pre_edges_num] = NULL ;
    //link junction and new edge.
    junction_node->succ_edges[junction_node->succ_edges_num] = junction_edge ;
    junction_node->succ_edges_num++ ;
    junction_node->succ_edges[junction_node->succ_edges_num] = NULL ;
    junction_edge->start_node = junction_node ;
    //link new edge and source node
    source->pre_edges[0] = junction_edge ;
    source->pre_edges_num = 1 ;
    source->pre_edges[source->pre_edges_num] = NULL ;
    junction_edge->end_node = source ;
    //return
    junction_node->node_type = JUNCTION ;
    return junction_node ;
}


//if the last exist token hasn't pointer to a node, link the need_node to the new_current_node.
void link_last_token(cfg_node_t *new_current_node, cfg_func_t *function) {
    token_list **need_token_prt = NULL ;
    /*token_list **true_token_prt = NULL ;*/
    case_t *temp_case = NULL ;
    int i ;
    //if there are new exist_token that hasn't been pointer to a node, then pointer to the new if node, and estimate whether has need_token pointer to the token, then link_nodes.
    if (function->exist_token_num > 0 && function->exist_tokens[function->exist_token_num - 1]->pointer == NULL) {
        function->exist_tokens[function->exist_token_num - 1]->pointer = new_current_node ;
        for (need_token_prt = function->need_tokens; *need_token_prt != NULL; need_token_prt++) {
            if(strcmp((*need_token_prt)->token_name, function->exist_tokens[function->exist_token_num - 1]->token_name) == 0) {
                if ((need_token_prt - function->need_tokens > 0) && ((*need_token_prt)->pointer->succ_edges_num == 0) && ((*(need_token_prt - 1))->pointer->node_id == (*need_token_prt)->pointer->node_id)) {
                    (*need_token_prt)->pointer->succ_edges_num++ ;
                    (*need_token_prt)->pointer->succ_edges[(*need_token_prt)->pointer->succ_edges_num] = NULL ;
                }

                link_nodes((*need_token_prt)->pointer, function->exist_tokens[function->exist_token_num - 1]->pointer, function) ;
                if ((*need_token_prt)->pointer->node_type == SWITCH_TEST) {
                    for (i = 0; i < (*need_token_prt)->pointer->switch_test_i->case_num; i++) {
                        if (strcmp((*need_token_prt)->pointer->switch_test_i->case_chain[i]->token_name, (*need_token_prt)->token_name) == 0) {
                            if ((*need_token_prt)->pointer->succ_edges_num != (i + 1)) {
                                temp_case = (*need_token_prt)->pointer->switch_test_i->case_chain[(*need_token_prt)->pointer->succ_edges_num - 1] ;
                                (*need_token_prt)->pointer->switch_test_i->case_chain[(*need_token_prt)->pointer->succ_edges_num - 1] = (*need_token_prt)->pointer->switch_test_i->case_chain[i] ;
                                (*need_token_prt)->pointer->switch_test_i->case_chain[i] = temp_case ;
                            }
                            break ;
                        }
                    }
                }
            }
        }
    }
}

cfg_node_t *creat_if_junction(cfg_node_t *temp_node, cfg_func_t *function) {
    int if_junction_token = 0 ;
    token_list **exist_token_prt = NULL ;
    token_list **need_token_prt = NULL ;
    cfg_node_t *new_junction = NULL ;
    for (exist_token_prt = function->exist_tokens; *exist_token_prt != NULL; exist_token_prt++) {
        if((*exist_token_prt)->pointer == NULL) {
            (*exist_token_prt)->pointer = temp_node ;
            for (need_token_prt = function->need_tokens; *need_token_prt != NULL; need_token_prt++) {
                if(strcmp((*need_token_prt)->token_name, (*exist_token_prt)->token_name) == 0) {
                    link_nodes((*need_token_prt)->pointer, (*exist_token_prt)->pointer, function) ;
                }
            }
            //if_junction_token = 1 ;
        }
    }
    //if there is an if junction, creat it.
    if (temp_node->pre_edges_num > 1) {
        new_junction = add_pre_junction(temp_node, function) ;
        new_junction->is_if_junction = true ;
    }
    return new_junction ;
}
//interpose a while junction between the if junction and it's succ junction.
cfg_node_t *add_while_junction(cfg_node_t *if_junc_node, cfg_func_t *function) {
    cfg_node_t *junction_node = NULL ;
    cfg_edge_t *junction_edge = NULL ;
    junction_node = new_node(function) ;
    junction_edge = new_edge(function) ;
    cfg_edge_t **source_pre_edges = NULL ;
    //link bottom if and new while junction.
    junction_node->succ_edges[junction_node->succ_edges_num] = junction_edge ;
    junction_node->succ_edges_num++ ;
    junction_node->succ_edges[junction_node->succ_edges_num] = NULL ;
    junction_edge->start_node = junction_node ;
    junction_edge->end_node = if_junc_node->succ_edges[0]->end_node ;
    if_junc_node->succ_edges[0]->end_node->pre_edges[0] = junction_edge ;
    //link if junction and new while junction
    junction_node->pre_edges[0] = if_junc_node->pre_edges[0] ;
    if_junc_node->pre_edges[0]->end_node = junction_node ;
    if_junc_node->succ_edges[0]->end_node = junction_node ;
    junction_node->pre_edges[1] = if_junc_node->succ_edges[0] ;
    junction_node->pre_edges_num = 2 ;
    junction_node->pre_edges[2] = NULL ;
    //dispose the pre_edges of if junction
    for(source_pre_edges = if_junc_node->pre_edges; *source_pre_edges != NULL; source_pre_edges++) {
        *source_pre_edges = *(source_pre_edges + 1) ;
    }
    if_junc_node->pre_edges_num-- ;
    //return
    junction_node->node_type = JUNCTION ;
    junction_node->is_if_junction = false ;
    junction_node->loop_times = LOOP_TIMES ;
    return junction_node ;

}

cfg_node_t *while_junction(cfg_node_t *if_node, cfg_func_t *function) {
    cfg_node_t *junction_node = NULL ;
    cfg_edge_t *junction_edge = NULL ;
    junction_node = new_node(function) ;
    junction_edge = new_edge(function) ;
    cfg_edge_t **source_pre_edges = NULL ;
    cfg_node_t *new_junction = NULL ;

    for(source_pre_edges = if_node->pre_edges + 1; *source_pre_edges != NULL; source_pre_edges++) {
        (*source_pre_edges)->end_node = junction_node;
        junction_node->pre_edges[junction_node->pre_edges_num] = *source_pre_edges ;
        junction_node->pre_edges_num++ ;
    }
    junction_node->pre_edges[junction_node->pre_edges_num] = NULL ;
    //link bottom if and new while junction.
    junction_node->succ_edges[junction_node->succ_edges_num] = junction_edge ;
    junction_node->succ_edges_num++ ;
    junction_node->succ_edges[junction_node->succ_edges_num] = NULL ;
    junction_edge->start_node = junction_node ;
    junction_edge->end_node = if_node ;
    if_node->pre_edges[1] = junction_edge ;
    if_node->pre_edges[2] = NULL ;

    new_junction = creat_if_junction(junction_node, function) ;
    //return
    junction_node->node_type = JUNCTION ;
    junction_node->is_if_junction = false ;
    junction_node->loop_times = LOOP_TIMES ;
    return junction_node ;

}
//if_test
void build_if_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) {
    //dispose the needless char
    int tail_handle ;
    int if_junction_token = 0 ;
    char *token = NULL ;
    char *pointer = NULL ;
    int row = 0 ;
    char *type_buffer[10] ;
    token_list **exist_token_prt = NULL ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    cfg_node_t *temp_node = NULL ;
    //split the string
    type_buffer[row] = strtok(line_str, " ") ;
    while (type_buffer[row] != NULL) {
        row++ ;
        type_buffer[row] = strtok(NULL, " ") ;
    }
    //new node if
    new_current_node = new_node(function) ;
    new_current_node->node_type = IF_TEST ;
    new_current_node->if_test_i = new_if() ;
    //if there are new exist_token that hasn't been pointer to a node, then pointer to the new if node, and estimate whether has need_token pointer to the token, then link_nodes.
    link_last_token(new_current_node, function) ;
    //link current_node and new if node
    if (current_node != NULL) {
        link_nodes(current_node, new_current_node, function) ;
    }
    /*            if (function->exist_token_num > 0 && function->exist_tokens[function->exist_token_num - 1]->pointer == NULL) {*/
    /*function->exist_tokens[function->exist_token_num - 1]->pointer = new_current_node ;*/
    /*for (need_token_prt = function->need_tokens; *need_token_prt != NULL; need_token_prt++) {*/
    /*if(strcmp(*need_token_prt->token_name, function->exist_tokens[function->exist_token_num - 1]->token_name) == 0) {*/
    /*link_nodes(*need_token_prt->pointer, function->exist_tokens[function->exist_token_num - 1]->pointer, function) ;*/
    /*}*/
    /*}*/
    /*}*/
    //find the need token of if node.
    //true token
    tail_handle = strlen(type_buffer[5]) ;
    type_buffer[5][tail_handle - 1] = '\0' ;
    pointer = type_buffer[5] ;
    for (exist_token_prt = function->exist_tokens; *exist_token_prt != NULL; exist_token_prt++) {
        if(strcmp((*exist_token_prt)->token_name, pointer) == 0) {
            link_nodes(new_current_node, (*exist_token_prt)->pointer, function) ;
            break ;
        }
    }
    //not an exist token
    if (*exist_token_prt == NULL) {
        add_need_token(pointer, new_current_node, function) ;
        //if there is if_junction, creat it.
        new_junction = creat_if_junction(new_current_node, function) ;
    }
    //is an exist token, then there is a loop, add junction_node(while junction)
    else {
        //goto point if_test_node, doesn't point while junction
        //generate if junction at the begin of the loop if need. if there are code like while(a < 1 || b > 2), then we need if junction.
        if ((*exist_token_prt)->pointer->node_type != JUNCTION && (*exist_token_prt)->pointer->pre_edges_num > 1) {
            new_junction = creat_if_junction((*exist_token_prt)->pointer, function) ;
            (*exist_token_prt)->pointer = new_junction ;
        }
        //add while junction
        new_junction = while_junction((*exist_token_prt)->while_pointer->succ_edges[0]->end_node, function) ;

        //goto point to while junction.
/*        //generate if junction at the begin of the loop if need. if there are code like while(a < 1 || b > 2), then we need if junction.*/
        /*if ((*exist_token_prt)->pointer->node_type != JUNCTION && (*exist_token_prt)->pointer->pre_edges_num > 1) {*/
            /*new_junction = creat_if_junction((*exist_token_prt)->pointer, function) ;*/
            /*(*exist_token_prt)->pointer = new_junction ;*/
        /*}*/
        /*//add while junction*/
        /*if ((*exist_token_prt)->while_pointer->succ_edges[0]->end_node->pre_edges_num >= 3) {*/
            /*new_junction = add_while_junction((*exist_token_prt)->while_pointer->succ_edges[0]->end_node, function) ;*/
        /*}*/
        /*else if ((*exist_token_prt)->while_pointer->succ_edges[0]->end_node->pre_edges_num == 2) {*/
            /*(*exist_token_prt)->while_pointer->succ_edges[0]->end_node->is_if_junction = false ;*/
            /*(*exist_token_prt)->while_pointer->succ_edges[0]->end_node->loop_times = LOOP_TIMES ;*/
        /*}*/
        /*else {*/
            /*perror("add while junction error!!") ;*/
            /*exit(EXIT_FAILURE) ;*/
        /*}*/

    }
    /* //estimate whether there is a if junction.*/
    /*if (new_junction != NULL) {*/
        /*temp_node = new_junction ;*/
    /*}*/
    /*else {*/
        /*temp_node = new_current_node ;*/
    /*}*/
    /*            for (exist_token_prt = function->exist_tokens; *exist_token_prt != NULL; exist_token_prt++) {*/
    /*if(*exist_token_prt->pointer == NULL) {*/
    /**exist_token_prt->pointer = temp_node ;*/
    /*for (need_token_prt = function->need_tokens; *need_token_prt != NULL; need_token_prt++) {*/
    /*if(strcmp(*need_token_prt->token_name, *exist_token_prt->token_name) == 0) {*/
    /*link_nodes(*need_token_prt->pointer, *exist_token_prt->pointer, function) ;*/
    /*}*/
    /*}*/
    /*if_junction_token = 1 ;*/
    /*}*/
    /*}*/
    /*//if there is an if junction, creat it.*/
    /*if (if_junction_token == 1) {*/
    /*new_junction = add_pre_junction(temp_node, function) ;*/
    /*new_junction->is_if_junction = true ;*/
    /*}*/
    //false token
    tail_handle = strlen(type_buffer[8]) ;
    type_buffer[8][tail_handle - 1] = '\0' ;
    pointer = type_buffer[8] ;
    add_need_token(pointer, new_current_node, function) ;
    //cmp_a
    //
    pointer = type_buffer[1] ;
    pointer++ ;
    //estimate whether cmp_a is a var, if right return the var position in string.
    token = is_instant_number(pointer) ;
    if (token != NULL) {
        new_current_node->if_test_i->a_is_var = false ;
        new_current_node->if_test_i->cmp_a = token ;
    }
    else {
        token = get_var_position(pointer, function, current_domain) ;
        if (token == NULL) {
            perror("UNKNOWN string!!!") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->if_test_i->a_is_var = true ;
        new_current_node->if_test_i->cmp_a = token ;
    }

    /*array_token = strchr(type_buffer[1], '.') ;*/
    /*if (array_token != NULL && !(type_buffer[1][1] == 'D' && type_buffer[1][2] == '.')) {*/
    /**array_token = '\0' ;*/
    /*}*/
    /*pointer = type_buffer[1] ;*/
    /*pointer++ ;*/
    /*if (*pointer >= '0' && *pointer <= '9') {*/
    /*new_current_node->if_test_i->a_is_var = false ;*/
    /*new_current_node->if_test_i->cmp_a = copy_string(pointer) ;*/
    /*}*/
    /*else {*/
    /*for (var_table = function->func_vars_table; *var_table != NULL; var_table++) {*/
    /*if (strcmp(*var_table->name, pointer) == 0 && var_table->effect_domain <= current_domain) {*/
    /*if (*var_table->effect_domain > temp_domain) {*/
    /*temp_var = var_table - function->func_vars_table ;*/
    /*temp_domain = *var_table->effect_domain ;*/
    /*}*/
    /*}*/
    /*}*/
    /*sprintf(var_type_buffer, "%d", temp_var) ;*/
    /*}*/

    //cmp_operand
    new_current_node->if_test_i->cmp_operand = copy_string(type_buffer[2]) ;

    //cmp_b
    tail_handle = strlen(type_buffer[3]) ;
    type_buffer[3][tail_handle - 1] = '\0' ;
    pointer = type_buffer[3] ;
    token = is_instant_number(pointer) ;
    if (token != NULL) {
        new_current_node->if_test_i->b_is_var = false ;
        new_current_node->if_test_i->cmp_b = token ;
    }
    else {
        token = get_var_position(pointer, function, current_domain) ;
        if (token == NULL) {
            perror("UNKNOWN string!!!") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->if_test_i->b_is_var = true ;
        new_current_node->if_test_i->cmp_b = token ;
    }

    /*array_token = strchr(type_buffer[3], '.') ;*/
    /*if (array_token != NULL && !(type_buffer[3][0] == 'D' && type_buffer[3][1] == '.')) {*/
    /**array_token = '\0' ;*/
    /*}*/
    /*pointer = type_buffer[3] ;*/
    /*if (*pointer >= '0' && *pointer <= '9') {*/
    /*new_current_node->if_test_i->b_is_var = false ;*/
    /*new_current_node->if_test_i->cmp_b = copy_string(pointer) ;*/
    /*}*/
    /*else {*/
    /*for (var_table = function->func_vars_table; *var_table != NULL; var_table++) {*/
    /*if (strcmp(*var_table->name, pointer) == 0 && var_table->effect_domain <= current_domain) {*/
    /*if (*var_table->effect_domain > temp_domain) {*/
    /*temp_var = var_table - function->func_vars_table ;*/
    /*temp_domain = *var_table->effect_domain ;*/
    /*}*/
    /*}*/
    /*}*/
    /*new_current_node->if_test_i->a_is_var = true ;*/
    /*sprintf(var_type_buffer, "%d", temp_var) ;*/
    /*new_current_node->if_test_i->cmp_a = copy_string(var_type_buffer) ;*/
    /*}*/
}



cfg_node_t *make_assign_call(char *line_str, cfg_node_t *current_node, cfg_func_t *function, cfg_func_t **functions, int current_domain) {
    //dispose the needless char
    int tail_handle ;
    char *token = NULL ;
    char *pointer = NULL ;
    int row = 0 ;
    int func_number ;
    int i = 0 ;
    int var_type = -1 ;
    int var_position ;

    char const **sys_type = NULL ;
    call_parameter *new_call_pmr = NULL ;
    //max input_argument is 20, so the row is 23
    char var_type_buffer[MAX_TYPE_NAME] ;
    char *type_buffer[MAX_INPUT_VAR + 3] ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    //split the string
    type_buffer[row] = strtok(line_str, " ") ;
    while (type_buffer[row] != NULL) {
        row++ ;
        type_buffer[row] = strtok(NULL, " ") ;
    }
    row-- ;
    //new_current_node
    new_current_node = new_node(function) ;
    //call have no destination
    if (type_buffer[1][0] == '(') {
        func_number = is_known_func(type_buffer[0], functions) ;
        if (func_number == -1) {
            new_current_node->node_type = UNKNOWN_CALL ;
        }
        else {
            new_current_node->node_type = CALL ;
            new_current_node->call_i = new_call() ;
            new_current_node->call_i->func_number = func_number ;
            new_current_node->call_i->dst_name = -1 ;
            i = 1 ;
            while (i <= row) {
                token = type_buffer[i] ;
                if (i == 1) {
                    token++ ;
                }
                tail_handle = strlen(token) ;
                if (token[tail_handle - 1] == ';') {
                    token[tail_handle - 2] = '\0' ;
                }
                else if (token[tail_handle - 1] == ',') {
                    token[tail_handle - 1] = '\0' ;
                }
                //estimate an actual_parameter and generate the call_parameter in the actual_parameter set
                if (*token != '\0') {
                    new_call_pmr = new_call_parameter() ;
                    pointer = is_instant_number(token) ;
                    if (pointer != NULL) {
                        new_call_pmr->var_number = pointer ;
                        new_call_pmr->is_var = false ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = new_call_pmr ;
                        new_current_node->call_i->parameter_num++ ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = NULL ;
                    }
                    else {
                        pointer = get_var_position(token, function, current_domain) ;
                        if (pointer == NULL) {
                            perror("call parameter is unknown!!") ;
                            exit(EXIT_FAILURE) ;
                        }
                        new_call_pmr->var_number = pointer ;
                        new_call_pmr->is_var = true ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = new_call_pmr ;
                        new_current_node->call_i->parameter_num++ ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = NULL ;
                    }
                }
                i++ ;
            }
        }
    }
    //call have destination
    else if (row >= 3 && type_buffer[3][0] == '(') {
        func_number = is_known_func(type_buffer[2], functions) ;
        if (func_number == -1) {
            new_current_node->node_type = UNKNOWN_CALL ;
        }
        else {
            new_current_node->node_type = CALL ;
            new_current_node->call_i = new_call() ;
            new_current_node->call_i->func_number = func_number ;
            pointer = get_var_position(type_buffer[0], function, current_domain) ;
            if (pointer == NULL) {
                perror("call dst is unknown!!") ;
                exit(EXIT_FAILURE) ;
            }
            new_current_node->call_i->dst_name = atoi(pointer) ;
            i = 3 ;
            while (i <= row) {
                token = type_buffer[i] ;
                if (i == 3) {
                    token++ ;
                }
                tail_handle = strlen(token) ;
                if (token[tail_handle - 1] == ';') {
                    token[tail_handle - 2] = '\0' ;
                }
                else if (token[tail_handle - 1] == ',') {
                    token[tail_handle - 1] = '\0' ;
                }
                //estimate an actual_parameter and generate the call_parameter in the actual_parameter set
                if (*token != '\0') {
                    new_call_pmr = new_call_parameter() ;
                    pointer = is_instant_number(token) ;
                    if (pointer != NULL) {
                        new_call_pmr->var_number = pointer ;
                        new_call_pmr->is_var = false ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = new_call_pmr ;
                        new_current_node->call_i->parameter_num++ ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = NULL ;
                    }
                    else {
                        pointer = get_var_position(token, function, current_domain) ;
                        if (pointer == NULL) {
                            perror("call parameter is unknown!!") ;
                            exit(EXIT_FAILURE) ;
                        }
                        new_call_pmr->var_number = pointer ;
                        new_call_pmr->is_var = true ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = new_call_pmr ;
                        new_current_node->call_i->parameter_num++ ;
                        new_current_node->call_i->actual_parameter[new_current_node->call_i->parameter_num] = NULL ;
                    }
                }
                i++ ;
            }
        }
    }
    //compulsory type convert
    else if (row >= 3 && type_buffer[2][0] == '(' && type_buffer[1][0] == '=') {
        new_current_node->node_type = ASSIGNMENT ;
        new_current_node->assignment_i = new_assignment() ;
        new_current_node->assignment_i->is_type_convert = true ;
        //dst
        pointer = get_var_position(type_buffer[0], function, current_domain) ;
        if (pointer == NULL) {
            perror("compulsory type convert dst is unknown!!") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->assignment_i->dst_name = atoi(pointer) ;
        //convert type
        var_type_buffer[0] = '\0' ;
        for (i = 2; i < row; i++) {
            token = strcat(var_type_buffer, type_buffer[i]) ;
            tail_handle = strlen(var_type_buffer) ;
            var_type_buffer[tail_handle] = ' ' ;
            var_type_buffer[tail_handle + 1] = '\0' ;
        }
        var_type_buffer[strlen(var_type_buffer) - 2] = '\0' ;
        token = var_type_buffer ;
        token++ ;
        for(sys_type = sys_var_type; *sys_type != NULL; sys_type++) {
            if (strcmp(token, *sys_type) == 0) {
                var_type = sys_type - sys_var_type ;
            }
        }
        if (var_type == -1) {
            perror("compulsory type is not a system type!!!") ;
            exit(EXIT_FAILURE) ;
        }
        var_type_buffer[0] = '\0' ;
        sprintf(var_type_buffer, "%d", var_type) ;
        new_current_node->assignment_i->operator_a = copy_string(var_type_buffer) ;
        //source var
        token = type_buffer[row] ;
        tail_handle = strlen(token) ;
        token[tail_handle - 1] = '\0' ;
        pointer = get_var_position(token, function, current_domain) ;
        if (pointer == NULL) {
            perror("compulsory type convert src is unknown!!") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->assignment_i->operator_b = pointer ;
        new_current_node->assignment_i->b_is_var = true ;
    }

    //assignment c = a + b
    else if (row == 4 && (type_buffer[3][0] == '+' || type_buffer[3][0] == '-' || type_buffer[3][0] == '*' || type_buffer[3][0] == '/')) {
        new_current_node->node_type = ASSIGNMENT ;
        new_current_node->assignment_i = new_assignment() ;
        new_current_node->assignment_i->is_type_convert = false ;
        pointer = get_var_position(type_buffer[0], function, current_domain) ;
        if (pointer == NULL) {
            perror("assignment dst is unknown!!") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->assignment_i->dst_name = atoi(pointer) ;
        //operator_a
        token = type_buffer[2] ;
        pointer = is_instant_number(token) ;
        if (pointer != NULL) {
            new_current_node->assignment_i->operator_a = pointer ;
            new_current_node->assignment_i->a_is_var = false ;
        }
        else {
            pointer = get_var_position(token, function, current_domain) ;
            if (pointer == NULL) {
                perror("assignment operator_a is unknown!!") ;
                exit(EXIT_FAILURE) ;
            }
            new_current_node->assignment_i->operator_a = pointer ;
            new_current_node->assignment_i->a_is_var = true ;
        }
        //operator_b
        token = type_buffer[4] ;
        tail_handle = strlen(token) ;
        token[tail_handle - 1] = '\0' ;
        pointer = is_instant_number(token) ;
        if (pointer != NULL) {
            new_current_node->assignment_i->operator_b = pointer ;
            new_current_node->assignment_i->b_is_var = false ;
        }
        else {
            pointer = get_var_position(token, function, current_domain) ;
            if (pointer == NULL) {
                perror("assignment operator_b is unknown!!") ;
                exit(EXIT_FAILURE) ;
            }
            new_current_node->assignment_i->operator_b = pointer ;
            new_current_node->assignment_i->b_is_var = true ;
        }
        //operand
        pointer = copy_string(type_buffer[3]) ;
        new_current_node->assignment_i->operand = pointer ;
    }
    //a = {} useless assignment
    else if (row == 2 && type_buffer[2][0] == '{' && type_buffer[2][1] == '}') {
        free(new_current_node) ;
        new_current_node = NULL ;
        return new_current_node ;
    }
    //assignment c = a
    else if (row == 2) {
        new_current_node->node_type = ASSIGNMENT ;
        new_current_node->assignment_i = new_assignment() ;
        new_current_node->assignment_i->is_type_convert = false ;
        //dst
        pointer = is_array(type_buffer[0], function, current_domain) ;
        if (pointer != NULL) {
            new_current_node->assignment_i->dst_name = atoi(pointer) ;
            new_current_node->assignment_i->has_array = 1 ;
            //i = get_array_num(type_buffer[0]) ;
            token = strchr(type_buffer[0], '[') ;
            token++ ;
            tail_handle = strlen(type_buffer[0]) ;
            type_buffer[0][tail_handle - 1] = '\0' ;
            pointer = is_instant_number(token) ;
            if (pointer != NULL) {
                new_current_node->assignment_i->offset_is_var = false ;
                new_current_node->assignment_i->array_offset = pointer ;
            }
            else {
                pointer = get_var_position(token, function, current_domain) ;
                if (pointer == NULL) {
                perror("array offset var is unknown!!") ;
                exit(EXIT_FAILURE) ;
                }
                new_current_node->assignment_i->array_offset = pointer ;
                new_current_node->assignment_i->offset_is_var = true ;
            }
        }
        else {
            pointer = get_var_position(type_buffer[0], function, current_domain) ;
            if (pointer == NULL) {
                perror("assignment dst var is unknown!!") ;
                exit(EXIT_FAILURE) ;
            }
            new_current_node->assignment_i->dst_name = atoi(pointer) ;
        }
        //operator_a
        tail_handle = strlen(type_buffer[2]) ;
        type_buffer[2][tail_handle - 1] = '\0' ;
        pointer = is_instant_number(type_buffer[2]) ;
        if (pointer != NULL) {
            new_current_node->assignment_i->operator_a = pointer ;
            new_current_node->assignment_i->a_is_var = false ;
        }
        else {
            new_current_node->assignment_i->a_is_var = true ;
            pointer = is_array(type_buffer[2], function, current_domain);
            if (pointer != NULL) {
                new_current_node->assignment_i->operator_a = pointer ;
                new_current_node->assignment_i->has_array = 2 ;
                token = strchr(type_buffer[2], '[') ;
                token++ ;
                tail_handle = strlen(type_buffer[2]) ;
                type_buffer[2][tail_handle - 1] = '\0' ;
                pointer = is_instant_number(token) ;
                if (pointer != NULL) {
                    new_current_node->assignment_i->offset_is_var = false ;
                    new_current_node->assignment_i->array_offset = pointer ;
                }
                else {
                    pointer = get_var_position(token, function, current_domain) ;
                    if (pointer == NULL) {
                        perror("array offset var is unknown!!") ;
                        exit(EXIT_FAILURE) ;
                    }
                    new_current_node->assignment_i->array_offset = pointer ;
                    new_current_node->assignment_i->offset_is_var = true ;
                }
            }
            else {
                pointer = get_var_position(type_buffer[2], function, current_domain) ;
                if (pointer == NULL) {
                    perror("assignment dst var is unknown!!") ;
                    exit(EXIT_FAILURE) ;
                }
                new_current_node->assignment_i->operator_a = pointer ;
            }
        }
        if (new_current_node->assignment_i->a_is_var == true) {
            var_position = atoi(new_current_node->assignment_i->operator_a) ;
            if (new_current_node->assignment_i->dst_name == var_position) {
                free(new_current_node->assignment_i->operator_a) ;
                free(new_current_node->assignment_i->array_offset) ;
                free(new_current_node->assignment_i) ;
                free(new_current_node) ;
                new_current_node = NULL ;
            }
        }
    }
    else {
        perror("unknown assignment or call lexical!!") ;
        exit(EXIT_FAILURE) ;
    }

    //link node
    if (new_current_node != NULL) {
        link_last_token(new_current_node, function) ;
        //link current_node and new if node
        if (current_node != NULL) {
            link_nodes(current_node, new_current_node, function) ;
        }
        new_junction = creat_if_junction(new_current_node, function) ;
    }
    //return
    return new_current_node ;
}


cfg_node_t *creat_goto_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function) {
    int tail_handle ;
    char *pointer = NULL ;
    int row = 0 ;
    char *type_buffer[3] ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    //split the string
    type_buffer[row] = strtok(line_str, " ") ;
    while (type_buffer[row] != NULL) {
        row++ ;
        type_buffer[row] = strtok(NULL, " ") ;
    }
    //new node if
    new_current_node = new_node(function) ;
    new_current_node->node_type = GOTO ;
    //link last token if any.
    link_last_token(new_current_node, function) ;
    //link current_node and new if node
    if (current_node != NULL && current_node->node_type != GOTO) {
        link_nodes(current_node, new_current_node, function) ;
    }
    //if there is if_junction, creat it.
    new_junction = creat_if_junction(new_current_node, function) ;
    //add the token to need_token_table
    tail_handle = strlen(type_buffer[1]) ;
    type_buffer[1][tail_handle - 1] = '\0' ;
    pointer = type_buffer[1] ;
    add_need_token(pointer, new_current_node, function) ;
    //current_node clear
    return new_current_node ;
}

void creat_switch_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) {
    int tail_handle ;
    int iter = 4 ;
    char *pointer = NULL ;
    char *temp = NULL ;
    int row = 0 ;
    char *type_buffer[MAX_SWITCH_CASE * 2 + 2] ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    //split the string
    type_buffer[row] = strtok(line_str, " ") ;
    while (type_buffer[row] != NULL) {
        row++ ;
        type_buffer[row] = strtok(NULL, " ") ;
    }
    row-- ;

    new_current_node = new_node(function) ;
    new_current_node->node_type = SWITCH_TEST ;
    new_current_node->switch_test_i = new_switch() ;
    //if there are new exist_token that hasn't been pointer to a node, then pointer to the new if node, and estimate whether has need_token pointer to the token, then link_nodes.
    link_last_token(new_current_node, function) ;
    //link current_node and new if node
    if (current_node != NULL) {
        link_nodes(current_node, new_current_node, function) ;
    }
    //if there is if_junction, creat it.
    new_junction = creat_if_junction(new_current_node, function) ;
    //find the need token of if node.
    //true token
    tail_handle = strlen(type_buffer[1]) ;
    type_buffer[1][tail_handle - 1] = '\0' ;
    pointer = type_buffer[1] ;
    pointer++ ;
    temp = get_var_position(pointer, function, current_domain) ;
    if (temp == NULL) {
        perror("switch var is unknown") ;
        exit(EXIT_FAILURE) ;
    }
    new_current_node->switch_test_i->switch_var = atoi(temp) ;
    //default
    new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num] = new_case() ;

    tail_handle = strlen(type_buffer[3]) ;
    type_buffer[3][tail_handle - 1] = '\0' ;
    pointer = type_buffer[3] ;
    new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num]->case_number = 0 ;
    new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num]->token_name = copy_string(pointer) ;
    add_need_token(pointer, new_current_node, function) ;

    new_current_node->switch_test_i->case_num++ ;
    new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num] = NULL ;

    if (iter > row) {
        return ;
    }
    //case
    while (iter != row + 1) {
        new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num] = new_case() ;
        tail_handle = strlen(type_buffer[iter + 1]) ;
        type_buffer[iter + 1][tail_handle - 1] = '\0' ;
        pointer = type_buffer[iter + 1] ;
        new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num]->case_number = atoi(pointer) ;

        tail_handle = strlen(type_buffer[iter + 2]) ;
        type_buffer[iter + 2][tail_handle - 1] = '\0' ;
        pointer = type_buffer[iter + 2] ;
        new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num]->token_name = copy_string(pointer) ;
        add_need_token(pointer, new_current_node, function) ;

        new_current_node->switch_test_i->case_num++ ;
        new_current_node->switch_test_i->case_chain[new_current_node->switch_test_i->case_num] = NULL ;

        iter = iter + 3 ;
    }

}

cfg_node_t *creat_return_node(char *line_str, cfg_node_t *current_node, cfg_func_t *function, int current_domain) {
    int tail_handle ;
    char *pointer = NULL ;
    char *temp = NULL ;
    int row = 0 ;
    char *type_buffer[3] ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    //split the string
    type_buffer[row] = strtok(line_str, " ") ;
    while (type_buffer[row] != NULL) {
        row++ ;
        type_buffer[row] = strtok(NULL, " ") ;
    }

    new_current_node = new_node(function) ;
    new_current_node->node_type = RETURN ;
    new_current_node->return_i = new_return() ;

    tail_handle = strlen(type_buffer[1]) ;
    pointer = type_buffer[1] ;
    type_buffer[1][tail_handle - 1] = '\0' ;
    temp = is_instant_number(pointer) ;
    if (temp != NULL) {
        new_current_node->return_i->return_is_var = false ;
        new_current_node->return_i->return_num = copy_string(temp) ;
    }
    else {
        temp = get_var_position(pointer, function, current_domain) ;
        if (temp == NULL) {
            perror("return var is unknown") ;
            exit(EXIT_FAILURE) ;
        }
        new_current_node->return_i->return_is_var = true ;
        new_current_node->return_i->return_num = temp ;
    }
    //link node
    link_last_token(new_current_node, function) ;
    //link current_node and new if node
    if (current_node != NULL) {
        link_nodes(current_node, new_current_node, function) ;
    }
    new_junction = creat_if_junction(new_current_node, function) ;
    return new_current_node ;

}


void build_cfg_tree(FILE *fp, cfg_func_t *function, cfg_func_t **functions) {
    //start
    int ch ;
    //first string buffer
    char var_type_buffer[MAX_TYPE_NAME] ;

    //effect_domain
    int range_stack[MAX_RANGE_DEPTH], top = 1 ;
    range_stack[0] = 0 ;
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
    char goto_test_s[] = "goto" ;
    char finally_var[] = "finally" ;
    char return_s[] = "return" ;

    //estimate whether is sys_type to define whether is declaration
    int var_type = -1 ;
    char const **sys_type = NULL ;

    //read a line from src file
    int line_tail ;
    char line_buffer[MAX_LINE_LENGTH] ;
    char *line_pointer = NULL ;
    char *var_buffer_token = NULL ;
    char *line_str = NULL ;

    //put input_argument to func_vars_table
    call_argument **input_argument = NULL ;
    declaration_t *new_dec = NULL ;
    declaration_t **var_table = NULL ;
    //token
    /*int exist_token_num = 0 ;*/
    /*int need_token_num = 0 ;*/
    /*token_list *exist_tokens[MAX_TOKEN_NUM] ;*/
    /*token_list *need_tokens[MAX_TOKEN_NUM] ;*/
    /*token_list **need_token_prt = NULL ;*/
    /*token_list **exist_token_prt = NULL ;*/
    /*exist_tokens[0] = NULL ;*/
    /*need_tokens[0] = NULL ;*/

    //current node
    cfg_node_t *current_node = NULL ;
    cfg_node_t *new_current_node = NULL ;
    cfg_node_t *new_junction = NULL ;
    cfg_node_t *exit_node = NULL ;
    /*cfg_edge_t *new_link_edge = NULL ;*/

    //set entry
    function->pre_entry = new_edge(function) ;
    current_node = new_node(function) ;
    current_node->node_type = ENTRY ;
    current_node->pre_edges[current_node->pre_edges_num] = function->pre_entry ;
    current_node->pre_edges_num++ ;
    current_node->pre_edges[current_node->pre_edges_num] = NULL ;
    function->pre_entry->end_node = current_node ;

    //put input_argument to the func_vars_table
    for(input_argument = function->input_argument; *input_argument != NULL; input_argument++) {
        new_dec = new_declaration() ;
        new_dec->name = copy_string((*input_argument)->arg_name) ;
        new_dec->variable_type = (*input_argument)->arg_type ;
        new_dec->is_pointer = (*input_argument)->is_pointer ;
        new_dec->is_struct = (*input_argument)->is_struct ;
        new_dec->struct_name = copy_string((*input_argument)->struct_name) ;
        new_dec->effect_domain = 1 ;
        function->func_vars_table[function->var_num] = new_dec ;
        function->var_num++ ;
        function->func_vars_table[function->var_num] = NULL ;
    }
    //put global variable to the func_vars_table
    if (strcmp(functions[0]->func_name, "global") == 0) {
        for(var_table = functions[0]->func_vars_table; *var_table != NULL; var_table++) {
            new_dec = new_declaration() ;
            new_dec->name = copy_string((*var_table)->name) ;
            new_dec->variable_type = (*var_table)->variable_type ;
            new_dec->is_pointer = (*var_table)->is_pointer ;
            new_dec->is_struct = (*var_table)->is_struct ;
            new_dec->struct_name = copy_string((*var_table)->struct_name) ;
            new_dec->array_len = (*var_table)->array_len ;
            new_dec->is_array = (*var_table)->is_array ;
            new_dec->is_static = (*var_table)->is_static ;
            new_dec->effect_domain = 0 ;
            function->func_vars_table[function->var_num] = new_dec ;
            function->var_num++ ;
            function->func_vars_table[function->var_num] = NULL ;
        }
    }
    //first '{'
    fgets(line_buffer, MAX_LINE_LENGTH, fp);
    range_num++ ;
    range_stack[top++] = range_num ;
    current_domain = range_num ;


    while (range_stack[top-1] != 0) {
        //get line and get the first string
        fgets(line_buffer, MAX_LINE_LENGTH, fp);
        if (line_buffer[0] == '\n') {
            continue ;
        }
        line_pointer = line_buffer ;
        var_buffer_token = var_type_buffer ;
        while (*line_pointer == ' ') line_pointer++ ;
        line_str = line_pointer ;
        while (*line_pointer != ' ' && *line_pointer != '\n') {
            *var_buffer_token = *line_pointer ;
            var_buffer_token++ ;
            line_pointer++ ;
        }
        *var_buffer_token = '\0' ;
        //remove the useless \n from the tail of the string
        line_str[strlen(line_str) - 1] = '\0' ;
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
        else if (strcmp(var_type_buffer, try_var) == 0 && strcmp(var_type_buffer, line_str) == 0) {
            has_try = 1 ;
        }
        else if (strcmp(var_type_buffer, finally_var) == 0 && strcmp(var_type_buffer, line_str) == 0) {
            while (strcmp(line_pointer, right_bracket) != 0) {
                fgets(line_buffer, MAX_LINE_LENGTH, fp);
                line_buffer[strlen(line_buffer) - 1] = '\0' ;
                line_pointer = line_buffer ;
                while (*line_pointer == ' ') {
                    line_pointer++ ;
                }
            }
        }
        else if (strcmp(var_type_buffer, right_bracket) == 0) {
            top-- ;
            current_domain = range_stack[top-1] ;
        }
        //if_test
        else if (strcmp(var_type_buffer, if_test_s) == 0) {
            build_if_node(line_str, current_node, function, current_domain) ;
            current_node = NULL ;
        }

        //switch_test
        else if (strcmp(var_type_buffer, switch_test_s) == 0) {
            creat_switch_node(line_str, current_node, function, current_domain) ;
            current_node = NULL ;
        }

        //junction_t
        else if (var_type_buffer[0] == '<' && var_type_buffer[1] == 'D') {
            line_str[strlen(line_str) - 1] = '\0' ;
            add_exist_token(line_str, function) ;
            //function->exist_tokens[function->exist_token_num]->token_name = copy_string(line_str) ;
            //function->exist_tokens[function->exist_token_num]->pointer = NULL ;
            if (current_node != NULL && current_node->node_type == GOTO) {
                function->exist_tokens[function->exist_token_num - 1]->while_pointer = current_node ;
                current_node = NULL ;
            }
            //function->exist_token_num++ ;
            //function->exist_tokens[function->exist_token_num] = NULL ;
        }
        //goto
        else if (strcmp(var_type_buffer, goto_test_s) == 0) {
            new_current_node = creat_goto_node(line_str, current_node, function) ;
            current_node = new_current_node ;
        }
        //return
        else if (strcmp(var_type_buffer, return_s) == 0) {
            new_current_node = creat_return_node(line_str, current_node, function, current_domain) ;
            current_node = NULL ;
        }
        //declaration_t and assignment_t and call_t
        else {
            for(sys_type = sys_var_type; *sys_type != NULL; sys_type++) {
                if (strcmp(var_type_buffer, *sys_type) == 0) {
                    var_type = sys_type - sys_var_type ;
                }
            }
            //declaration_t, except enum
            if (var_type != -1) {
                build_vars_table(line_str, function, var_type, current_domain) ;
            }
            //assignment and call
            else {
                new_current_node = make_assign_call(line_str, current_node, function, functions, current_domain) ;
                if (new_current_node != NULL) {
                    current_node = new_current_node ;
                }
            }
            var_type = -1 ;
        }
    }

    //set exit
    exit_node = new_node(function) ;
    exit_node->node_type = EXIT ;
    link_last_token(exit_node, function) ;
    if (current_node != NULL) {
        link_nodes(current_node, exit_node, function) ;
    }
    if (new_current_node->node_type == RETURN) {
        link_nodes(new_current_node, exit_node, function) ;
    }
    new_junction = creat_if_junction(exit_node, function) ;

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


    //
}


//cfg_func_t **build_cfgs(char *cfg_file, char *glob_var_file) {
cfg_func_t **build_cfgs(char *cfg_file) {
    FILE *fp ;
    fp = fopen(cfg_file, "r") ;
    if (fp == NULL) {
        perror("file open error!!!") ;
        exit(EXIT_FAILURE) ;
    }

    char func_name_buffer[MAX_FUNC_NAME] ;
    char row_buffer[MAX_LINE_LENGTH] ;
    char *func_name ;
    cfg_func_t **result_cfgs = NULL ;
    cfg_func_t **functions = new_functions() ;
    int func_num = 0 ;
    int ch ;

    fseek(fp, 0, SEEK_SET);
    //generate function_table
    while ((ch = fgetc(fp)) != EOF) {
        if (ch != ' ' && ch != '{' && ch != '}' && ch != '\n') {
            ungetc(ch, fp) ;
            functions[func_num] = new_func() ;
            //get function name
            fscanf(fp,"%s", func_name_buffer) ;
            func_name = copy_string(func_name_buffer) ;
/*            if (func_num == 0 && strcmp(func_name, "global") != 0) {*/
                /*perror("the first function isn't global function!") ;*/
                /*exit(EXIT_FAILURE) ;*/
            /*}*/
            functions[func_num]->func_name = func_name ;
            functions[func_num]->func_num = func_num ;
            func_num++ ;
        }
        if (ch != '\n') {
            fgets(row_buffer, MAX_LINE_LENGTH, fp) ;
        }
    }
    functions[func_num] = NULL ;

    fseek(fp, 0, SEEK_SET);

    for (func_num = 0; functions[func_num] != NULL; func_num++) {
        fscanf(fp,"%s", func_name_buffer) ;
        //store input arguments
        build_input_args(fp, functions[func_num]) ;
        //build_function cfg_tree
        build_cfg_tree(fp, functions[func_num], functions) ;
        //skim the useless chars
        while ((ch = fgetc(fp)) == '\n') ;
        ungetc(ch, fp) ;
    }



    fclose(fp) ;

    result_cfgs = functions ;
    return result_cfgs ;
}

