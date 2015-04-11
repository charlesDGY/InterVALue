objects = main.o interval.o common.o intervalset.o cfg.o edgecontext.o

edit : $(objects)
	gcc -Wall -g $(objects) -o edit -lm

main.o : interval.h intervalset.h edgecontext.h cfg.h
interval.o : common.h

.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

