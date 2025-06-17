#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#define ARRAY_SIZE (64 * 1024 * 1024)
#define PAGE_SIZE 4096
#define SEQUENTIAL_ITERATIONS 100
#define RANDOM_ITERATIONS 1000000

double get_time_diff(struct timeval start, struct timeval end) {
  return (end.tv_sec - start.tv_sec) +
         (end.tv_usec - start.tv_usec) / 1000000.0;
}

void sequential_access_test(int *array, int size) {
  struct timeval start, end;
  volatile long sum = 0;

  gettimeofday(&start, NULL);

  for (int iter = 0; iter < SEQUENTIAL_ITERATIONS; iter++) {
    for (int i = 0; i < size; i++) {
      sum += array[i];
    }
  }

  gettimeofday(&end, NULL);
  double sequential_time = get_time_diff(start, end);
  printf("Sequential access time: %.6f seconds\n", sequential_time);
}

void random_access_test(int *array, int size) {
  struct timeval start, end;
  volatile long sum = 0;

  int *indices = malloc(RANDOM_ITERATIONS * sizeof(int));
  srand(42);
  for (int i = 0; i < RANDOM_ITERATIONS; i++) {
    indices[i] = rand() % size;
  }

  gettimeofday(&start, NULL);

  for (int i = 0; i < RANDOM_ITERATIONS; i++) {
    sum += array[indices[i]];
  }

  gettimeofday(&end, NULL);
  double random_time = get_time_diff(start, end);
  printf("Random access time: %.6f seconds\n", random_time);

  free(indices);
}

int main(int argc, char *argv[]) {
  printf("TLB Effects Demonstration\n");
  printf("Array size: %d elements (%d MB)\n", ARRAY_SIZE,
         ARRAY_SIZE * 4 / (1024 * 1024));

  int *array = malloc(ARRAY_SIZE * sizeof(int));
  if (array == NULL) {
    perror("malloc failed");
    return 1;
  }

  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = i;
  }

  if (argc > 1) {
    if (strcmp(argv[1], "sequential") == 0) {
      sequential_access_test(array, ARRAY_SIZE);
    } else if (strcmp(argv[1], "random") == 0) {
      random_access_test(array, ARRAY_SIZE);
    }
    free(array);
    return 0;
  }

  printf("\nSequential vs Random Memory Access:\n");
  sequential_access_test(array, ARRAY_SIZE);
  random_access_test(array, ARRAY_SIZE);

  printf("\nTo observe dTLB-load-misses with perf:\n");
  printf(
      "  perf stat -e dTLB-load-misses,dTLB-loads ./tlb_effects sequential\n");
  printf("  perf stat -e dTLB-load-misses,dTLB-loads ./tlb_effects random\n");

  free(array);
  return 0;
}
