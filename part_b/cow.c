#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

void print_memory_usage(const char *label) {
  FILE *status = fopen("/proc/self/status", "r");
  if (!status) {
    perror("fopen");
    return;
  }

  char line[256];
  long vm_size = 0, vm_rss = 0;

  while (fgets(line, sizeof(line), status)) {
    if (strncmp(line, "VmSize:", 7) == 0) {
      sscanf(line, "VmSize: %ld kB", &vm_size);
    } else if (strncmp(line, "VmRSS:", 6) == 0) {
      sscanf(line, "VmRSS: %ld kB", &vm_rss);
    }
  }
  fclose(status);

  printf("%s - PID: %d, VmSize: %ld KB, VmRSS: %ld KB\n", label, getpid(),
         vm_size, vm_rss);
}

int main() {
  printf("Copy-On-Write Demonstration\n");

  size_t size = 10 * 1024 * 1024;
  char *memory = malloc(size);
  memset(memory, 'A', size);

  printf("Parent allocated %zu MB\n", size / (1024 * 1024));
  print_memory_usage("Parent before fork");

  pid_t pid = fork();

  if (pid == 0) {
    printf("\n=== Child Process (PID: %d) ===\n", getpid());
    print_memory_usage("Child after fork (before COW)");

    sleep(2);

    printf("Child: Writing to trigger COW...\n");
    for (size_t i = 0; i < size; i += 4096) {
      memory[i] = 'B';
    }

    print_memory_usage("Child after COW writes");
    sleep(2);

    printf("Child: COW triggered\n");
    exit(0);
  } else {
    printf("\n=== Parent Process (PID: %d) ===\n", getpid());
    printf("Child PID: %d\n", pid);
    print_memory_usage("Parent after fork (sharing memory)");

    sleep(3);

    wait(NULL);
    print_memory_usage("Parent after child completes");
    printf("COW demonstration complete\n");
  }

  free(memory);
  return 0;
}
