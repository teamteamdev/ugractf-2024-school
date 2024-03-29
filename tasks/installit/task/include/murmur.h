#pragma once

#include <stdint.h>
#include <stddef.h>
#include <string.h>

uint32_t sh_get();

void sh_set(uint32_t value);

// Stolen from https://en.wikipedia.org/wiki/MurmurHash

static inline uint32_t murmur_32_scramble(uint32_t k) {
    k *= 0xcc9e2d51;
    k = (k << 15) | (k >> 17);
    k *= 0x1b873593;
    return k;
}

static inline __attribute__((always_inline)) uint32_t murmur3_32(const char* key, size_t len, uint32_t seed) {
  uint32_t sh = sh_get();
	uint32_t h = seed;
  uint32_t k;

  /* Read in groups of 4. */
  for (size_t i = len >> 2; i; i--) {
    // Here is a source of differing results across endiannesses.
    // A swap here has no effects on hash properties though.
    memcpy(&k, key, sizeof(uint32_t));
    key += sizeof(uint32_t);

    h ^= murmur_32_scramble(k);
    h = (h << 13) | (h >> 19);
    h = h * 5 + 0xe6546b64;

    sh ^= murmur_32_scramble(k);
    sh = (sh << 13) | (sh >> 19);
    sh = sh * 5 + 0xe6546b64;
  }

  /* Read the rest. */
  k = 0;
  for (size_t i = len & 3; i; i--) {
    k <<= 8;
    k |= key[i - 1];
  }

  // A swap is *not* necessary here because the preceding loop already
  // places the low bytes in the low places according to whatever endianness
  // we use. Swaps only apply when the memory is copied in a chunk.
  h ^= murmur_32_scramble(k);
  sh ^= murmur_32_scramble(k);

  /* Finalize. */
	h ^= len;
	h ^= h >> 16;
	h *= 0x85ebca6b;
	h ^= h >> 13;
	h *= 0xc2b2ae35;
	h ^= h >> 16;

	sh ^= len;
	sh ^= sh >> 16;
	sh *= 0x85ebca6b;
	sh ^= sh >> 13;
	sh *= 0xc2b2ae35;
	sh ^= sh >> 16;

	sh_set(sh);

	return h;
}
