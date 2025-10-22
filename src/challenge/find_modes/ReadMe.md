
Peter
[proposes](https://github.com/jhanley634/dojo-blackboard/issues/86)
that we find the mode(s) of a million random integers that have restricted range.

There's at least two approaches.

1. Sort, with O(N log N) cost, then scan for long runs, similar to [RLE](https://en.wikipedia.org/wiki/Run-length_encoding).
2. Count, with O(N) cost, similar to [radix sort](https://en.wikipedia.org/wiki/Radix_sort), since there's at most only a thousand distinct values.
