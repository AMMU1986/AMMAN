/*
 * Problem 3: Divide and Conquer Sorting - MERGE SORT (recursive)
 * --------------------------------------------------------------
 * Chosen algorithm: MERGE SORT.
 *
 * Strategy (divide and conquer):
 *   DIVIDE  : split the array into two halves about the midpoint.
 *   CONQUER : recursively merge-sort each half.
 *   COMBINE : merge the two sorted halves into one sorted array.
 *
 * What we count:
 *   KEY COMPARISONS performed during the MERGE step, i.e. each time two
 *   elements from the left and right halves are compared (left[i] <= right[j]).
 *   This is stated clearly in the output.
 *
 * Complexities (merge sort):
 *   Best    : O(n log n)
 *   Average : O(n log n)
 *   Worst   : O(n log n)   (always divides in half, always merges)
 * Auxiliary space: O(n) for the temporary merge buffers
 *   (plus O(log n) recursion stack).
 */

#include <stdio.h>

static long comparisons = 0;   /* global key-comparison counter */

/*
 * merge - combine sorted arr[l..m] and arr[m+1..r] into one sorted run.
 */
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int left[n1], right[n2];

    for (int i = 0; i < n1; i++) left[i]  = arr[l + i];
    for (int j = 0; j < n2; j++) right[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        comparisons++;                 /* count comparison left[i] vs right[j] */
        if (left[i] <= right[j]) {
            arr[k++] = left[i++];
        } else {
            arr[k++] = right[j++];
        }
    }
    /* copy any remaining elements (no further key comparisons needed) */
    while (i < n1) arr[k++] = left[i++];
    while (j < n2) arr[k++] = right[j++];
}

/*
 * mergeSort - recursive divide-and-conquer sort of arr[l..r].
 */
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;   /* DIVIDE */
        mergeSort(arr, l, m);      /* CONQUER left  */
        mergeSort(arr, m + 1, r);  /* CONQUER right */
        merge(arr, l, m, r);       /* COMBINE */
    }
}

void printArray(const char *label, int arr[], int n) {
    printf("%s", label);
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

int main(void) {
    /* At least 10 integers. */
    int arr[] = {38, 27, 43, 3, 9, 82, 10, 1, 56, 24, 17};
    int n = (int)(sizeof(arr) / sizeof(arr[0]));

    printArray("Before sorting : ", arr, n);

    mergeSort(arr, 0, n - 1);

    printArray("After sorting  : ", arr, n);
    printf("Counted quantity: key comparisons during merge = %ld\n", comparisons);

    printf("\nMerge Sort complexity: best/avg/worst = O(n log n).\n");
    printf("Auxiliary space: O(n) buffers + O(log n) recursion stack.\n");
    return 0;
}
