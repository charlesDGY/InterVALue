objects = common.o interval.o intervalset.o cfg.o edgecontext.o rangeanalysis.o main.o
edit : $(objects)
	gcc -Wall $(objects) -g -o edit -lm

common.o : common.c
	gcc -g -c common.c
interval.o : interval.c
	gcc -g -c interval.c
intervalset.o : intervalset.c
	gcc -g -c intervalset.c
cfg.o : cfg.c
	gcc -g -c cfg.c
edgecontext.o : edgecontext.c
	gcc -g -c edgecontext.c
rangeanalysis.o : rangeanalysis.c
	gcc -g -c rangeanalysis.c
main.o : main.c rangeanalysis.h
	gcc -g -c main.c

.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

