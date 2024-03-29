#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "code.h"
#include "murmur.h"

int patch(const char* fname, uint32_t from, uint32_t to) {
  FILE* f = fopen(fname, "r+b");
  uint32_t number = 0;
  while (1) {
    number <<= 8;
    int readed = fread(&number, 1, 1, f);
    if (readed == 0) {
      break;
    }

    if (number == from) {
      fseek(f, -4, SEEK_CUR);
      fwrite(&to, 4, 1, f);
      fprintf(stderr, "patched from %x to %x at %lx\n", from, to, ftell(f) - 4);
    }
  }
  int err = ferror(f);
  fclose(f);
  return err;
}

int main(int argc, const char* argv[]) {
  if (argc != 3) {
    fprintf(stderr, "usage: %s <fname> <seed>\n", argv[0]);
    return 1;
  }


  uint32_t seed = strtoul(argv[2], NULL, 0);
  fprintf(stderr, "seed = 0x%x\n", seed);

  if (patch(argv[1], 0xefbeadde, seed)) {
    fputs("failed patch seed\n", stderr);
    return 1;
  }

  char* code = NULL;
  size_t code_size;
  int err = get_code(argv[1], &code, &code_size);
  if (err != 0) {
    fprintf(stderr, "failed hash code: %d\n", err);
    return err;
  }
  uint32_t hash = murmur3_32(code, code_size, 0);
  fprintf(stderr, "hashed `%s`: 0x%x\n", argv[1], hash);

  if (patch(argv[1], 0xbebafeca, hash)) {
    fputs("failed patch hash\n", stderr);
    return 1;
  }

  printf("0x%x\n", hash);
}
