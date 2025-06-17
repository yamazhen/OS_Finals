#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

volatile int running = 1;
void stop(int sig) {
  (void)sig;
  running = 0;
}

int main() {
  signal(SIGINT, stop);
  printf("Thrashing Demo - Press Ctrl+C to stop\n");

  size_t size = 500 * 1024 * 1024;
  char *memory = malloc(size);

  while (running) {
    for (size_t i = 0; i < size && running; i += 4096) {
      memory[i] = 1;
    }
  }

  free(memory);
  printf("Thrashing demo stopped\n");
  return 0;
}
