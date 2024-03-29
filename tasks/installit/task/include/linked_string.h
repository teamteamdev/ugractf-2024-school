#pragma once

#include <stddef.h>

typedef struct linked_string_t {
  struct linked_string_t* previous;
  char* data;
  size_t total_size;
} linked_string_t;

linked_string_t *ls_concat(char* data, size_t size, linked_string_t* previous);

char* ls_to_string(linked_string_t* ls);
