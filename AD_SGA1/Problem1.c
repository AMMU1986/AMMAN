/*
 * Problem 1: Empirical Algorithm Analysis - Insertion Sort
 * -------------------------------------------------------
 * Strategy: Incremental (decrease-and-conquer) sorting.
 *
 * What we count as a "key comparison":
 *   Every comparison between the current key and an already-sorted
 *   array element, i.e. each evaluation of the condition (arr[j] > key).
 *   This is the dominant operation of insertion sort, so it is the
 *   fair quantity to measure empirically.
 *
 * We run the SAME-size input in three arrangements:
 *   - already sorted      (best case)
 *   - reverse sorted      (worst case)
 *   - randomly ordered    (average case)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10   /* common input size for all three cases */

/*
 * insertionSort - sorts arr[0..n-1] ascending.
 * Returns the number of key comparisons performed.
 */
long insertionSort(int arr[], int n) {
    long comparisons = 0;
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;

        /*
         * Each time we test (arr[j] > key) we count ONE key comparison,
         * including the test that finally fails and ends the loop.
         */
        while (j >= 0) {
            comparisons++;            /* count the comparison arr[j] > key */
            if (arr[j] > key) {
                arr[j + 1] = arr[j];  /* shift larger element right */
                j--;
            } else {
                break;                /* key is in place */
            }
        }
        arr[j + 1] = key;
    }
    return comparisons;
}

void printArray(const char *label, int arr[], int n) {
    printf("%s", label);
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

/* copy source[] into dest[] so each test uses identical data size */
void copyArray(int dest[], int src[], int n) {
    for (int i = 0; i < n; i++) dest[i] = src[i];
}

int main(void) {
    int work[N];

    /* ---- Case 1: already sorted ---- */
    int sorted[N] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    copyArray(work, sorted, N);
    printArray("Already-sorted input : ", work, N);
    long c1 = insertionSort(work, N);
    printArray("  Sorted output       : ", work, N);
    printf("  Key comparisons       : %ld\n\n", c1);

    /* ---- Case 2: reverse sorted ---- */
    int reversed[N] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    copyArray(work, reversed, N);
    printArray("Reverse-sorted input : ", work, N);
    long c2 = insertionSort(work, N);
    printArray("  Sorted output       : ", work, N);
    printf("  Key comparisons       : %ld\n\n", c2);

    /* ---- Case 3: random order ---- */
    srand((unsigned) time(NULL));
    int random[N];
    for (int i = 0; i < N; i++) random[i] = rand() % 100;
    copyArray(work, random, N);
    printArray("Random input         : ", work, N);
    long c3 = insertionSort(work, N);
    printArray("  Sorted output       : ", work, N);
    printf("  Key comparisons       : %ld\n\n", c3);

    /* ---- Theoretical reference ---- */
    printf("Theoretical comparison bounds for n = %d:\n", N);
    printf("  Best  case (sorted)  : n-1            = %d\n", N - 1);
    printf("  Worst case (reverse) : n(n-1)/2       = %d\n", N * (N - 1) / 2);
    printf("\nComplexity: best case O(n), worst/average case O(n^2).\n");
    printf("Space complexity: O(1) auxiliary (in-place).\n");

    return 0;
}
