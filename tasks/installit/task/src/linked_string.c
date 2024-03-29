#include <string.h>
#include <stdlib.h>

#include "linked_string.h"

linked_string_t *ls_concat(char* data, size_t size, linked_string_t* previous) {
  linked_string_t* ls = (linked_string_t*) malloc(sizeof(struct linked_string_t));
  ls->previous = previous;
  ls->data = data;
  ls->total_size = size + (previous == NULL ? 0 : previous->total_size);
  return ls;
}

char* ls_to_string(linked_string_t* ls) {
  size_t total_size = ls->total_size;
  char* ptr = malloc(total_size + 1);
  if (!ptr) {
    return NULL;
  }

  while (ls) {
    size_t ls_size = ls->total_size - (ls->previous == NULL ? 0 : ls->previous->total_size);
    memcpy(ptr + ls->total_size - ls_size, ls->data, ls_size);
    ls = ls->previous;
  }

  ptr[total_size] = 0;

  return ptr;
}
