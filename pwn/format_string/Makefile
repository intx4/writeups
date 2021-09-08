CC=gcc
CFLAGS=-mpreferred-stack-boundary=2 -no-pie -z -fno-stack-protector -ggdb -m32
DEPS = shellcode.h

default: sploit.o target.o
	$(CC) $(CFLAGS) -o target target.c 
	$(CC) $(CFLAGS) -o sploit sploit.c
.PHONY = clean

clean:
	rm *.c

