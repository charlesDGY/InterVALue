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

#ifndef NEW_RANGEANALYSIS_H
#define NEW_RANGEANALYSIS_H

#include "rangeanalysis.h"

cfg_func_t **get_cfg(char *program_str, int *num) ;
edge_context *new_range_analysis(edge_context *input_arg, int fp, cfg_func_t **result_cfg, int i) ;

#endif
