/* MDH WCET BENCHMARK SUITE. File version $Id: insertsort.c,v 1.3 2005/11/11 10:30:41 ael01 Exp $ */

/*************************************************************************/
/*                                                                       */
/*   SNU-RT Benchmark Suite for Worst Case Timing Analysis               */
/*   =====================================================               */
/*                              Collected and Modified by S.-S. Lim      */
/*                                           sslim@archi.snu.ac.kr       */
/*                                         Real-Time Research Group      */
/*                                        Seoul National University      */
/*                                                                       */
/*                                                                       */
/*        < Features > - restrictions for our experimental environment   */
/*                                                                       */
/*          1. Completely structured.                                    */
/*               - There are no unconditional jumps.                     */
/*               - There are no exit from loop bodies.                   */
/*                 (There are no 'break' or 'return' in loop bodies)     */
/*          2. No 'switch' statements.                                   */
/*          3. No 'do..while' statements.                                */
/*          4. Expressions are restricted.                               */
/*               - There are no multiple expressions joined by 'or',     */
/*                'and' operations.                                      */
/*          5. No library calls.                                         */
/*               - All the functions needed are implemented in the       */
/*                 source file.                                          */
/*                                                                       */
/*                                                                       */
/*************************************************************************/
/*                                                                       */
/*  FILE: insertsort.c                                                   */
/*  SOURCE : Public Domain Code                                          */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     Insertion sort for 10 integer numbers.                            */
/*     The integer array a[] is initialized in main function.            */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

/* Changes:
 * JG 2005/12/12: Indented program.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "intervaltest.h"


#ifdef DEBUG
int             cnt1, cnt2;
#endif

#define MAX 32767

int glob ;
float glob2 = 4.5 ;

typedef struct node2 {
    int p;
    int j;
    struct node2 *next;
} node2;


/*int add(int a, int b) {*/
    /*int c = a + b ;*/
    /*return c ;*/
/*}*/

int sub(int a, int b) {
    long d = a - b ;
    return d ;
}

typedef struct node3{
    int a ;
} node3 ;

int
hoho(int i)
{
/*    {*/
        /*int woca = 9 ;*/
        /*long cao = 32 ;*/
    /*}*/
    long long youma = 4 ;
    unsigned long long youmei = 2 ;
    char ee = 's', as = 'c';
    if (ee == as) {
        ee = 'c' ;
    }
    int D = 3 ;
    glob = 1 ;
    if (glob2 - 10 == glob) {
        glob2 = 4 ;
    }
    int val = 12, val2 = 6;
    int gg = 2 - val ;
    int j = MAX;
    j = (val + val2) * val2 - val ;
    if (i > 0 && j<50) {
        while (j < 100) {
            j = j + 5;
        }
    }
    else {
        j--;
    }

    if (val == 5) {
        val++ ;
        val2 = val % 2 ;
    }


    int a[50] ;
    a[10] = 100 ;
    a[39] = 23 ;
    a[val] = 4 ;
    if (a[10] == 100) {
        a[32] = 3 ;
    }

    node3 newnode ;
    newnode.a = 4 ;
    node2 *node44 = (node2 *)malloc(sizeof(node2)) ;
    node44->p = 5 ;
    node44->j = 10 ;

    int *kk =(int *) malloc(sizeof(int));
    kk = &j ;
    int *point = kk ;
    if (*point != 5) {
        printf("\n");
    }

    float noteasy = 0.0578 ;

    double t = 5 ;
    float haha = 10 ;
    unsigned short k = 5u ;
    unsigned long kj = 2ul ;


    typedef struct cang cang ;
    struct cang {
        int l ;
    } ;

    cang zzz = {10} ;
    enum hhh {
        MONDAY, THURSDAY
    };
    enum hhh hoes = THURSDAY ;
    float noha = 0.05 ;
    unsigned int pp= 9 ;
    unsigned long poi= 3 ;
    unsigned char pio= 'j' ;
    char ma ;
    if (k == 4) {
        printf("\n");
    }

    val = sub(add(i, j), val) ;
    while(i > 0) {
        switch (val) {
            case 3:
                i = j ;
                j = 2 ;
                break ;
            case 8:
                i = i + 1 ;
                j = 6 ;
                break ;
            default:
                i = 0 ;
        }
        i = -2 ;
    }
    i = sqrt(j) ;
    int vv = 4 ;
    double ss = 2.3 ;
    vv = floor(ss) ;
    printf("%d\n", j) ;
    return 0 ;
}
