objects = main.o interval.o common.o intervalset.o cfg.o edgecontext.o

edit : $(objects)
	gcc -Wall $(objects) -g -o edit -lm

main.o : main.c interval.h intervalset.h edgecontext.h cfg.h
	gcc -g -c main.c
interval.o : interval.c common.h
	gcc -g -c interval.c
common.o : common.c
	gcc -g -c common.c
intervalset.o : intervalset.c
	gcc -g -c intervalset.c
cfg.o : cfg.c
	gcc -g -c cfg.c
edgecontext.o : edgecontext.c
	gcc -g -c edgecontext.c

.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

