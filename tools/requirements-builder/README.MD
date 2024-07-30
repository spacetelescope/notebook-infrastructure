# About
This tool is intended for use with science platforms (e.g. TIKE). It attempts to find the most essential packages for an arbitrary collection of notebooks; we want the maximum number of passing notebooks for N included packages.

## Potential Improvements
- The solution presented by this tool is convenient, but not entirely correct. A full solution likely requires some clever use of "nearest neighbors", or maybe graph theory. (actually, this wouldn't be too bad. For N notebooks, there would be N(N-1)/2 distance comparisons to make. eliminating the furthest notebook and recomputing the necessary packages should be the maximally efficient algorithm.
- just generally having a programmer look at poorly-written astronomer code
