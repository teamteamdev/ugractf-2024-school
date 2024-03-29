#pragma once

#include "linked_string.h"

typedef struct iterator_state_t iterator_state_t;

iterator_state_t* it_alloc();
iterator_state_t* it_step(iterator_state_t* it, char** output);
