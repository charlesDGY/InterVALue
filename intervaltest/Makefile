objects = intervaltest.o

edit : $(objects)
	gcc -fdump-tree-cfg-lineno $(objects) -o edit -lm

intervaltest.o : intervaltest.h

.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

