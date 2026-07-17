PROGNAME=echotunnel
CC=gcc
CFLAGS= -O2 -Wall
OBJ= icmp.o echotunnel.o tunnel.o
.c.o:
	$(CC) -c $(CFLAGS) $<

all: $(PROGNAME)

$(PROGNAME): $(OBJ) Makefile
	$(CC) -O2 -Wall -o $(PROGNAME) $(OBJ)
	strip $(PROGNAME)

dep: clean
	$(CC) -MM *.c > Makefile.dep

clean:
	rm -f *.o $(PROGNAME)

include Makefile.dep
