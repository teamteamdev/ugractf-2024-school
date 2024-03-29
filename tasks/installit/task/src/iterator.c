#include <string.h>
#include <stdlib.h>

#include "iterator.h"

#define LOCS_SIZE 8
#define NAMES_SIZE 8
#define MAX_DEPTH 1
#define PATH_SIZE 20

struct iterator_state_t {
  struct iterator_state_t* upper;
  linked_string_t *prefix;
  size_t pos;
  size_t depth;
  char* path;
};

static char* known_locs[LOCS_SIZE] = {
  "/usr",
  "/bin",
  "/home",
  "/opt",
  "/local",
  "/etc",
  "/var",
  "/log"
};

static char* known_names[NAMES_SIZE] = {
  "/install_it",
  "/installit",
  "/not_a_flag",
  "/setup.exe",
  "/bash",
  "/cd",
  "/local",
  "/flag.txt",
};

iterator_state_t* it_alloc() {
  iterator_state_t* it = (iterator_state_t*) malloc(sizeof(struct iterator_state_t));
  it->upper = NULL;
  it->prefix = NULL;
  it->pos = 0;
  it->path = malloc(PATH_SIZE);
  it->depth = 0;
  return it;
}

size_t make_path(char* ptr, size_t pos, size_t depth) {
  char* name = known_names[pos % NAMES_SIZE];
  char* loc = known_locs[pos / NAMES_SIZE];

  strcpy(ptr, loc);
  strcpy(ptr + strlen(loc), name);
  size_t used = strlen(loc) + strlen(name);
  if (depth > 0) {
    while (used < PATH_SIZE) {
      ptr[used++] = rand() % (0x7E - 0x20) + 0x20;
    }
  }
  return used;
}

iterator_state_t* it_step(iterator_state_t* it, char** output) {
  free(*output);
  *output = NULL;
  if (!it) {
    return NULL;
  }

  it->pos++;
  if (it->pos > 2 * NAMES_SIZE * LOCS_SIZE) {
    iterator_state_t* upper = it->upper;
    free(it->path);
    free(it);
    return it_step(upper, output);
  }

  size_t path_size = make_path(it->path, (it->pos - 1) % (NAMES_SIZE * LOCS_SIZE), it->depth);
  linked_string_t *ls = ls_concat(it->path, path_size, it->prefix);

  if (it->pos > NAMES_SIZE * LOCS_SIZE) {
    if (it->depth > MAX_DEPTH) {
      return it_step(it, output);
    }

    iterator_state_t* inner = it_alloc();
    inner->upper = it;
    inner->prefix = ls;
    inner->depth = it->depth + 1;
    return it_step(inner, output);
  } else {
    *output = ls_to_string(ls);
    return it;
  }
}
