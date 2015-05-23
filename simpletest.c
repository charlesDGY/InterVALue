int global() {
    int glob1 = 1 ;
    int glob2 = 2 ;
}

int glob1 = 1 ;
int glob2 = 2 ;

int add(int a, int b) {
    int c ;
    int d ;
    glob1 = 5 ;
    c = a + b ;
    d = mul(c,glob1) ;
    return d ;
}

int mul(int a, int b) {
    return a * b ;
}

int f (int i)
{
/*    int j = 0;*/
    /*if (i > 0) {*/
        /*while (j < 10) {*/
            /*j = j + 5;*/
        /*}*/
    /*}*/
    /*else {*/
        /*j = j + 1;*/
    /*}*/
    /*while (j > 0) {*/
        /*switch (i) {*/
            /*case 3:*/
                /*i = 3 ;*/
                /*break ;*/
            /*case 4:*/
                /*i = 4 ;*/
            /*case 5:*/
                /*i = 5 ;*/
                /*break ;*/
            /*default:*/
                /*i = 6 ;*/
        /*}*/
        /*j-- ;*/
    /*}*/

    /*int a = 5 ;*/
    /*int b = 8 ;*/
    /*int c ;*/
    /*int d ;*/
    /*c = add(a, b) ;*/
    /*d = mul(c, b) ;*/
    /*glob2 = d ;*/
    int a = 1 ;
    int b = 7 ;
    while (a < 30) {
        while (b < a) {
            if (b > 5) {
                b = b * 3 ;
            }
            else {
                b = b + 2 ;
            }
            if (b >= 10 && b <= 12) {
                a = a + 10 ;
            }
            else {
                a = a + 1 ;
            }
        }
        a = a + 2 ;
        b = b - 10 ;
    }

    return 0 ;
}

