int f (int i)
{
    int j = 0;
    if (i > 0) {
        while (j < 10) {
            j = j + 5;
        }
    }
    else {
        j = j + 1;
    }
    while (j > 0) {
        switch (i) {
            case 3:
                i = 3 ;
                break ;
            case 4:
                i = 4 ;
            case 5:
                i = 5 ;
                break ;
            default:
                i = 6 ;
        }
        j-- ;
    }

    return i ;
}

