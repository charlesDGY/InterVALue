# InterVALue





## Conditions that haven’t been handled

> 1. the functions belonging to the c library couldn’t been handled.
    if they doesn’t effect the branch and concerned variables’s value, they can be ignored and we can obtain the result needed.
> 2. now it’s only allowed to define the most simple pointer variable `int *p` and the most simple array `int a[n]`.
> 3. it’s not allowed to define a function in another function.
> 4. actually, now we haven’t handled pointer and the assignments like `k = &j` and `*k = j` is not allowed.
> 5. enum type hasn’t been handled yet.
> 6. static type hasn’t been handled yet.
> 7. all functions and variables should be copied to one file as the input of the tool.(so there is no extern token)
> 8. `do_while`structure is not allowed yet.
> 9. the function is only distinguished by their names(the number of their input arguments can’t distinguish them yet).
> 10. if global variables exist, we should creat a new function named “global” at the beginning of the source code and put global variables
    declaration and initialization in it. So we don’t allow the normal first source code function to be named as “global”.
