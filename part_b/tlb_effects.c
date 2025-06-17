#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#define ARRAY_SIZE (16 * 1024 * 1024)
#define PAGE_SIZE 4096
#define ITERATIONS 1000000

double get_time_diff(struct timeval start, struct timeval end) {
  return (end.tv_sec - start.tv_sec) +
         (end.tv_usec - start.tv_usec) / 1000000.0;
}

void sequential_access_test(int *array, int size) {
  struct timeval start, end;
  volatile int sum = 0;

  printf("Sequential Memory Access Test...\n");
  gettimeofday(&start, NULL);

  for (int iter = 0; iter < ITERATIONS / 1000; iter++) {
    for (int i = 0; i < size; i++) {
      sum += array[i];
    }
  }

  gettimeofday(&end, NULL);
  double sequential_time = get_time_diff(start, end);
  printf("Sequential access time: %.6f seconds (sum: %d)\n", sequential_time,
         sum);
}

void random_access_test(int *array, int size) {
  struct timeval start, end;
  volatile int sum = 0;

  printf("Random Memory Access Test...\n");

  int *indices = malloc(ITERATIONS * sizeof(int));
  srand(time(NULL));
  for (int i = 0; i < ITERATIONS; i++) {
    indices[i] = rand() % size;
  }

  gettimeofday(&start, NULL);

  for (int i = 0; i < ITERATIONS; i++) {
    sum += array[indices[i]];
  }

  gettimeofday(&end, NULL);
  double random_time = get_time_diff(start, end);
  printf("Random access time: %.6f seconds (sum: %d)\n", random_time, sum);

  free(indices);
}

int main() {
  printf("TLB Effects Demonstration\n");
  printf("Array size: %d elements (%d MB)\n", ARRAY_SIZE,
         ARRAY_SIZE * 4 / (1024 * 1024));
  printf("Run with perf to observe TLB misses:\n");
  printf("  perf stat -e dTLB-load-misses,dTLB-loads ./partb_tlb_effects\n\n");

  int *array = malloc(ARRAY_SIZE * sizeof(int));
  if (array == NULL) {
    perror("malloc failed");
    return 1;
  }

  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = i;
  }

  printf("=== Memory Access Pattern Comparison ===\n");

  sequential_access_test(array, ARRAY_SIZE);
  printf("\n");

  random_access_test(array, ARRAY_SIZE);
  printf("\n");

  printf("\nExpected behavior:\n");
  printf("- Sequential access: High TLB hit rate, low dTLB-load-misses\n");
  printf("- Random access: Low TLB hit rate, high dTLB-load-misses\n");

  free(array);
  return 0;
}
