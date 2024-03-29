#include "murmur.h"

static uint32_t sh_value;

uint32_t sh_get() {
  return sh_value;
}

void sh_set(uint32_t value) {
  sh_value = value;
}
