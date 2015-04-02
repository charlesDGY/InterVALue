objects = main.o interval.o common.o intervalset.o

edit : $(objects)
	gcc -fdump-tree-vcg-lineno $(objects) -o edit -lm

main.o : interval.h intervalset.h
interval.o : common.h


.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

