#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "iterator.h"
#include "murmur.h"
#include "code.h"

static char* code = NULL;
static size_t code_size = 0;

int main(int argc, const char* argv[]) {
  unsigned seed = strtoul(argv[2], NULL, 0);
  unsigned code_hash = strtoul(argv[3], NULL, 0);
  const char* fname = argv[1];

  fprintf(stderr, "seed = 0x%x, code_hash = 0x%x\n", seed, code_hash);

  srand(seed);
  sh_set(seed);

  int err;
  if ((err = get_code(fname, &code, &code_size)) != 0) {
    fprintf(stderr, "failed find installation at `%s`, error %s\n", fname, strerror(err));
  }
  if (murmur3_32(code, code_size, 0) != code_hash) {
    fprintf(stderr, "invalid hash of `%s`\n", fname);
    exit(7);
  }

  iterator_state_t* it = it_alloc();
  char* path = NULL;

  while ((it = it_step(it, &path)) != NULL) {
    murmur3_32(path, strlen(path), 0);
    murmur3_32(code, code_size, 0);
  }

  printf("ugra_y0u_1nstall3d_it_%x\n", sh_get());
  return 0;
}
