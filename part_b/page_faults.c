#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

int main() {
  printf("Page Faults Demonstration\n\n");

  size_t size = 100 * 1024 * 1024;
  char *memory = malloc(size);
  for (size_t i = 0; i < size; i += 4096) {
    memory[i] = 1;
  }
  printf("Minor faults: malloc + access\n");
  free(memory);

  FILE *fp = tmpfile();
  size_t file_size = 10 * 1024 * 1024;
  char buffer[1024];
  memset(buffer, 'A', 1024);
  for (size_t i = 0; i < file_size / 1024; i++) {
    fwrite(buffer, 1, 1024, fp);
  }

  void *mapped = mmap(NULL, file_size, PROT_READ, MAP_SHARED, fileno(fp), 0);
  char *mapped_char = (char *)mapped;
  for (size_t i = 0; i < file_size; i += 4096) {
    volatile char c = mapped_char[i];
    (void)c;
  }
  printf("Major faults: mmap file access\n");

  munmap(mapped, file_size);
  fclose(fp);
  return 0;
}
