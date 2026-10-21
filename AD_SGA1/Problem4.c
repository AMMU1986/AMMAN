/*
 * Problem 4: Fractional Knapsack - GREEDY strategy
 * ------------------------------------------------
 * Strategy: Greedy by decreasing value/weight ratio.
 *
 * Why greedy is correct here:
 *   Because items are DIVISIBLE, taking as much as possible of the
 *   highest value-per-unit-weight item can never be worse than any
 *   alternative: any unit of capacity is best filled by the remaining
 *   item with the largest ratio. This "exchange argument" guarantees the
 *   greedy choice leads to a globally optimal solution (unlike 0/1 knapsack).
 *
 * Time complexity: O(n log n), dominated by sorting the items by ratio.
 *                  The greedy selection pass is O(n).
 * Space complexity: O(1) auxiliary beyond the item list.
 */

#include <stdio.h>

typedef struct {
    int   id;
    int   weight;
    int   value;
    double ratio;    /* value / weight */
} Item;

/* Sort items by DECREASING value/weight ratio (simple selection sort). */
void sortByRatioDesc(Item items[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int best = i;
        for (int j = i + 1; j < n; j++) {
            if (items[j].ratio > items[best].ratio) best = j;
        }
        if (best != i) {
            Item tmp = items[i];
            items[i] = items[best];
            items[best] = tmp;
        }
    }
}

int main(void) {
    /* Given test data. */
    Item items[] = {
        {1, 10,  60, 0},
        {2, 20, 100, 0},
        {3, 30, 120, 0}
    };
    int n = (int)(sizeof(items) / sizeof(items[0]));
    double capacity = 50.0;   /* knapsack capacity */

    /* Step 1: compute value/weight ratio for every item. */
    for (int i = 0; i < n; i++)
        items[i].ratio = (double) items[i].value / items[i].weight;

    /* Step 2: sort in decreasing order of ratio. */
    sortByRatioDesc(items, n);

    printf("Knapsack capacity: %.0f\n\n", capacity);
    printf("%-6s %-8s %-8s %-10s %-10s\n",
           "Item", "Weight", "Value", "Ratio", "Fraction");

    double remaining = capacity;
    double totalValue = 0.0;

    /* Step 3: greedily select items. */
    for (int i = 0; i < n; i++) {
        double fraction;
        if (items[i].weight <= remaining) {
            fraction = 1.0;                 /* take the whole item */
            remaining  -= items[i].weight;
            totalValue += items[i].value;
        } else {
            fraction = remaining / items[i].weight;   /* take a fraction */
            totalValue += items[i].value * fraction;
            remaining = 0;
        }

        printf("%-6d %-8d %-8d %-10.2f %-10.2f\n",
               items[i].id, items[i].weight, items[i].value,
               items[i].ratio, fraction);

        if (remaining <= 0) {
            /* print remaining untouched items with fraction 0 for clarity */
            for (int k = i + 1; k < n; k++)
                printf("%-6d %-8d %-8d %-10.2f %-10.2f\n",
                       items[k].id, items[k].weight, items[k].value,
                       items[k].ratio, 0.0);
            break;
        }
    }

    printf("\nMaximum value achievable: %.2f\n", totalValue);
    /* Expected for capacity 50: 240.00 */
    return 0;
}
