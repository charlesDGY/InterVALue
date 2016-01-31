objects = common.o interval.o intervalset.o cfg.o edgecontext.o rangeanalysis.o new_range_analysis.o main.o
edit : $(objects)
	gcc -Wall $(objects) -g -o edit -lm

cfiles = common.c interval.c intervalset.c cfg.c edgecontext.c rangeanalysis.c new_range_analysis.c

new_range_analysis.so : $(cfiles)
	gcc -fPIC -shared -o new_range_analysis.so $(cfiles)

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

new_range_analysis.o : new_range_analysis.c
	gcc -g -c new_range_analysis.c

main.o : main.c new_range_analysis.h
	gcc -g -c main.c

.PHONY : clean link
clean:
	rm edit $(objects)
link :
	gcc $(objects) -o main -lm

