
---
title: python recursion
subtitle: It keeps getting better.
author: John Hanley
date: 30\textsuperscript{th} September 2025
geometry: paperwidth=8in, paperheight=6in
header-includes:
    - \usepackage{setspace}
    - \onehalfspacing
    - \usepackage{graphicx}
    - \usepackage{caption}
---
[//]: # ( Copyright 2025 John Hanley. MIT Licensed. )

\newcommand{\blank}{\vspace{4mm}\vfill}
\Large
\newpage
\hrule
\blank

# agenda

- recursion
- recursion in Scheme
- TCO
- stability
- python
- recent interpreters

\blank
\hrule
\newpage

# recursion

```
"""Recursively solve the famous Towers of Hanoi problem."""

Peg = str

def hanoi(n: int, source: Peg, target: Peg, aux: Peg) -> None:
    if n == 0:
        return  # base case
    hanoi(n - 1, source, aux, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, aux, target, source)

hanoi(3, "A", "C", "B")
```

# towers in motion

```
    hanoi(n - 1, source, aux, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, aux, target, source)
```
`hanoi(3, "A", "C", "B")`\blank
\begin{minipage}[t]{0.39\linewidth}

- Move disk 1 from A to C
- Move disk 2 from A to B
- Move disk 1 from C to B
- Move disk 3 from A to C
- Move disk 1 from B to A
- Move disk 2 from B to C
- Move disk 1 from A to C

\end{minipage}
\begin{minipage}[t]{0.2\linewidth}
\hspace*{4cm}\raisebox{-4.8cm}{\includegraphics[height=5cm]{tall-tower.jpg}}
\end{minipage}

# the lambda calculus

![](lisp_cycles.png){height=6cm}
\blank
```
#lang racket

(+ 1 2 3)
6
```

# factorial

[tail call optimization](https://en.wikipedia.org/wiki/Tail_call)

```
(define (fact-slow n)  ; TCO is disabled, so the call stack grows
  (if (zero? n)
      1
      (* n (fact-slow (sub1 n)))))


(fact-slow 5)
120
```
\newpage

# factorial

```
(define (fact-slow n)  ; TCO is disabled, so the call stack grows
  (if (zero? n)
      1
      (* n (fact-slow (sub1 n)))))

(define (fact n)
  (_fact n 1))

(define (_fact n acc)
  (if (zero? n)
      acc
      (_fact (sub1 n) (* acc n))))
```

# timing
\blank
```
Factorial 250000 found by #<procedure:fact-slow> in 29848 msec

Factorial 250000 found by #<procedure:fact>      in 10349 msec

```
\blank\hfill
![](https://asset.conrad.com/media10/isa/160267/c1/-/en/860048_BB_00_FB/image.jpg){height=4cm}

# stability -- ubuntu

![](ubuntu-versions.png)

# stability -- python interpreter

![](python-versions.png)

# image credits

- https://en.wikipedia.org/wiki/Tower_of_Hanoi
  - AlejandroLinaresGarcia:
  - https://en.wikipedia.org/wiki/File:UniversumUNAM34.JPG
- https://xkcd.com/297 -- Randall Munroe
- https://asset.conrad.com/media10/isa/160267/c1/-/en/860048_BB_00_FB/image.jpg
- https://en.wikipedia.org/wiki/Ubuntu_version_history
  - https://upload.wikimedia.org/wikipedia/en/timeline/swfdceo7tl9n28j9pamsv083nwmv0l7.png
- https://en.wikipedia.org/wiki/History_of_Python
  - https://upload.wikimedia.org/wikipedia/en/timeline/3aeqr87p1hb7nohu4c5lnlkdiiypums.png
