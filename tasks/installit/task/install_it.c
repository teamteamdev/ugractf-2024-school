#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "iterator.h"
#include "murmur.h"
#include "code.h"

static unsigned seed = 0xdeadbeef;
static volatile unsigned code_hash = 0xcafebabe;
static char* code = NULL;

void check_hash(const char* fname) {
  size_t code_size = 0;
  int err = 0;
  uint32_t hash;

  if ((err = get_code(fname, &code, &code_size)) != 0) {
    fprintf(stderr, "failed find installation at `%s`, error: %s\n", fname, strerror(err));
  } else if ((hash = murmur3_32(code, code_size, 0)) != code_hash) {
    fprintf(stderr, "failed validate installation at `%s`\n", fname);
    err = 7;
  }

  if (err != 0) {
    fprintf(stderr, "tip: you can install by `cp %s %s`\n", program_invocation_name, fname);
    exit(err);
  }
}

int main(int argc, const char* argv[]) {
  srand(seed);
  sh_set(seed);

  check_hash(argv[0]);

  iterator_state_t* it = it_alloc();
  char* path = NULL;

  while ((it = it_step(it, &path)) != NULL) {
    uint32_t path_hash = murmur3_32(path, strlen(path), 0);
    printf("checking path `%s`, hash = %08x...\n", path, path_hash);
    check_hash(path);
  }

  printf("Flag was installed. Flag value is `ugra_y0u_1nstall3d_it_%x`\n", sh_get());
  return 0;
}
