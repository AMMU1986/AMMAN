/*
 * Problem 2: Divide and Conquer - Maximum Subarray
 * ------------------------------------------------
 * Strategy: Divide and conquer.
 *   Split the array at the midpoint and recursively solve three cases:
 *     (a) maximum subarray lying entirely in the LEFT half
 *     (b) maximum subarray lying entirely in the RIGHT half
 *     (c) maximum subarray CROSSING the midpoint
 *   The answer for the current range is the best of the three.
 *
 * Indexing convention: indices are 0-BASED and both start and end are
 * INCLUSIVE, i.e. the subarray is arr[start .. end].
 *
 * Time  complexity: T(n) = 2T(n/2) + O(n)  =>  O(n log n)
 * Space complexity: O(log n) auxiliary, due to the recursion stack depth.
 */

#include <stdio.h>
#include <limits.h>

typedef struct {
    int sum;    /* best sum found              */
    int lo;     /* start index (inclusive)     */
    int hi;     /* end index   (inclusive)     */
} Result;

/*
 * maxCrossing - best subarray that MUST use arr[mid] and arr[mid+1],
 * i.e. it crosses the midpoint. Expands left from mid and right from mid+1.
 */
Result maxCrossing(int arr[], int low, int mid, int high) {
    int leftSum = INT_MIN, sum = 0, leftIdx = mid;
    for (int i = mid; i >= low; i--) {
        sum += arr[i];
        if (sum > leftSum) { leftSum = sum; leftIdx = i; }
    }

    int rightSum = INT_MIN, rightIdx = mid + 1;
    sum = 0;
    for (int j = mid + 1; j <= high; j++) {
        sum += arr[j];
        if (sum > rightSum) { rightSum = sum; rightIdx = j; }
    }

    Result r = { leftSum + rightSum, leftIdx, rightIdx };
    return r;
}

/*
 * maxSubarray - recursive divide-and-conquer driver for arr[low..high].
 */
Result maxSubarray(int arr[], int low, int high) {
    if (low == high) {                 /* base case: single element */
        Result r = { arr[low], low, high };
        return r;
    }

    int mid = low + (high - low) / 2;

    Result left  = maxSubarray(arr, low, mid);        /* case (a) */
    Result right = maxSubarray(arr, mid + 1, high);   /* case (b) */
    Result cross = maxCrossing(arr, low, mid, high);  /* case (c) */

    /* return the best of the three */
    if (left.sum >= right.sum && left.sum >= cross.sum) return left;
    if (right.sum >= left.sum && right.sum >= cross.sum) return right;
    return cross;
}

int main(void) {
    /* Classic CLRS test array (0-based indexing). */
    int arr[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int n = (int)(sizeof(arr) / sizeof(arr[0]));

    printf("Input array (0-based indices): ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    Result ans = maxSubarray(arr, 0, n - 1);

    printf("Maximum sum : %d\n", ans.sum);
    printf("Start index : %d (0-based)\n", ans.lo);
    printf("End index   : %d (0-based)\n", ans.hi);

    printf("Selected subarray: ");
    for (int i = ans.lo; i <= ans.hi; i++) printf("%d ", arr[i]);
    printf("\n");

    /* Expected: subarray {4, -1, 2, 1}, sum 6, indices 3..6. */
    return 0;
}
