#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

int main() {
  printf("Page Faults Demonstration\n\n");

  printf("1. Generating minor page faults with malloc...\n");
  size_t size = 100 * 1024 * 1024;
  char *memory = malloc(size);
  if (memory == NULL) {
    perror("malloc failed");
    return 1;
  }

  for (size_t i = 0; i < size; i += 4096) {
    memory[i] = 1;
  }
  printf("Minor faults: malloc + access completed\n");
  free(memory);

  printf("2. Generating major page faults with mmap...\n");

  int fd = open("/tmp/pagefault_test", O_CREAT | O_RDWR | O_TRUNC, 0644);
  if (fd == -1) {
    perror("open failed");
    return 1;
  }

  size_t file_size = 10 * 1024 * 1024;

  char buffer[4096];
  memset(buffer, 'A', sizeof(buffer));
  for (size_t written = 0; written < file_size; written += sizeof(buffer)) {
    size_t to_write = (file_size - written < sizeof(buffer))
                          ? (file_size - written)
                          : sizeof(buffer);
    if (write(fd, buffer, to_write) != (ssize_t)to_write) {
      perror("write failed");
      close(fd);
      unlink("/tmp/pagefault_test");
      return 1;
    }
  }

  fsync(fd);

  void *mapped = mmap(NULL, file_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (mapped == MAP_FAILED) {
    perror("mmap failed");
    close(fd);
    unlink("/tmp/pagefault_test");
    return 1;
  }

  char *mapped_char = (char *)mapped;
  volatile char sum = 0;
  for (size_t i = 0; i < file_size; i += 4096) {
    sum += mapped_char[i];
  }
  printf("Major faults: mmap file access completed (checksum: %d)\n", sum);

  munmap(mapped, file_size);
  close(fd);
  unlink("/tmp/pagefault_test");

  return 0;
}
