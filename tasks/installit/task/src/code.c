#include <stdlib.h>
#include <string.h>

#include <elf.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

#include "code.h"
#include "murmur.h"

int get_code(const char* fname, char** out, size_t *outsize) {
  int fd = open(fname, O_RDONLY);
  if (fd == -1) {
    return errno;
  }

  Elf64_Ehdr hdr;
  if (read(fd, &hdr, sizeof(Elf64_Ehdr)) == -1) {
    return errno;
  }
  if (lseek(fd, hdr.e_shoff, SEEK_SET) == (off_t) -1) {
    return errno;
  }

  if (hdr.e_ident[EI_CLASS] != ELFCLASS64) {
    close(fd);
    return -2;
  }
  Elf64_Shdr* sections = (Elf64_Shdr*) malloc(sizeof(Elf64_Shdr) * hdr.e_shnum);

  if (read(fd, sections, 64 * hdr.e_shnum) == -1) {
    free(sections);
    return errno;
  }
  Elf64_Shdr shdr = sections[hdr.e_shstrndx];

  char* strtab = (char*)malloc(shdr.sh_size);

  if (lseek(fd, shdr.sh_offset, SEEK_SET) == (off_t) -1) {
    free(strtab);
    free(sections);
    return errno;
  }
  if (read(fd, strtab, shdr.sh_size) == -1) {
    free(strtab);
    free(sections);
    return errno;
  }

  for (int i = 0; i < hdr.e_shnum; i++) {
    Elf64_Shdr curr = sections[i];
    if (curr.sh_type == SHT_PROGBITS && strncmp(strtab + curr.sh_name, ".text", 5) == 0) {
      if (lseek(fd, curr.sh_offset, SEEK_SET) == (off_t) -1) {
        free(strtab);
        free(sections);
        return errno;
      }

      free(*out);
      *outsize = curr.sh_size;
      *out = (char*)malloc(curr.sh_size);
      if (read(fd, *out, curr.sh_size) == -1) {
        free(strtab);
        free(sections);
        return errno;
      }

      free(strtab);
      free(sections);
      close(fd);
      return 0;
    }
  }

  free(strtab);
  free(sections);
  close(fd);

  return -1;
}
