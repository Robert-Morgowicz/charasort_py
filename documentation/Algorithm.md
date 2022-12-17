Charasort implements a simple merge sort algorithm, with the singular exception that instead of having a numeric compare function which assigns an ordering between objects in the list, the user acts as the compare function; deciding the ordering of elements based on their preference.  As such, the algorithm descripton is very similar to the basic merge sort:
1. The list of entries loaded from the image directory is decomposed into singleton lists of one element each:
```
[A, B, C, D, E ,F, G, H] -> [[A], [B], [C], [D], [E] ,[F], [G], [H]]
```
2. The list of lists is traversed.  The first two populated lists are compared against each other and the first elemet of each list is compared.  Each 'compare' queries the user to select the element.  When an element is selected, it is added to a new list which will contain the result of mergeing the two lists and removed from its current list.  If either list becomes empty, the remaining elements in the non-empty list are appended to the result list.  When both lists are empty, the next two lists are considered.  
```
Battle 01: A vs B
> user picks A
  v    v                                       v  v
[[A], [B], [C], [D], [E] ,[F], [G], [H]] -> [[], [B], [C], [D], [E] ,[F], [G], [H]] , [[A]]
             v    v
-> [[], [], [C], [D], [E] ,[F], [G], [H]]  ,  [[A, B]]
...
Battle 04: G vs H
> user picks H
                          v    v
[[], [], [], [], [] ,[], [G], [H]] -> [[], [], [], [], [] ,[], [], []] , [[A, B], [D, C], [E, F], [H, G]]
Battle 05: A vs D
> user picks D
[[A, B], [D, C], [E, F] , [H, G]] -> [[A, B], [C], [E, F] , [H, G]] , [[D]]
Battle 06: A vs C
> user picks A
[[A, B], [C], [E, F] , [H, G]] , [[D]] -> [[B], [C], [E, F] , [H, G]] , [[D, A]]
Battle 07: B vs C
> user picks B
[[B], [C], [E, F] , [H, G]] , [[D, A]] -> [[], [C], [E, F] , [H, G]] , [[D, A, B]]
-> [[], [], [E, F] , [H, G]] , [[D, A, B, C]]
...
```
This pattern continues until there is a single list containing all elemets in a sorted order.  
```
...
Battle n: H vs C
> user picks C
[[H, G], [C]] , [[D, A, B, E, F]] -> [[H, G], []] , [[D, A, B, E, F, C]]
-> [[], []] , [[D, A, B, E, F, C, H, G]]
-> [D, A, B, E, F, C, H, G]
```