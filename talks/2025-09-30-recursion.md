
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

\vfill
\begin{center}
Connect with me at https://www.linkedin.com/in/jhanley714
\end{center}

\newcommand{\blank}{\vspace{4mm}\vfill}
\Large
\newpage
\hrule
\blank

# agenda

- improvements
- recursion
- recursion in Scheme
- TCO
- stability
- python
- recent interpreters

\blank
\hrule
\newpage

# transparent improvements

\blank

- diverse speedups, in libs and interpreter
- quadratic string append
- bare `except` vs. CTRL/C
- timsort speed from Tim Peters
- `dict` storage & iteration order from Raymond Hettinger
- "zero cost" `try:` blocks, also by Raymond

\blank
\newpage

# quadratic $O(n^2)$ [string append](https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuilder.html#append-java.lang.CharSequence-)

```
    n = 1_000_000
    s = ""
    for _ in range(n):
        s += " hello"
    return s
```
\vfill
_versus_
\vfill
```
    text = []
    for _ in range(n):
	    text.append(" hello")

	return "".join(text)
```
\blank
\newpage

# coming soon

\blank

Interpreter 3.14 hits the streets October 7\textsuperscript{th}.

\vspace{1cm}

It will feature
[template t-strings](https://peps.python.org/pep-0750/#motivation),
similar to formatted f-strings.

\blank
\newpage

# motivation

\blank

StackOverflow question:

> [Why does python limit recursion depth?](https://stackoverflow.com/questions/79770935/why-does-python-limit-recursion-depth-and-how-is-this-limit-decided#79770941)

\blank

# cheaper, lazy Python frames

\blank

Buried in the
[3.11 rel notes](https://docs.python.org/3/whatsnew/3.11.html#faster-runtime)
we find:

\blank

> - Streamlined the internal frame struct to contain only essential information

> For most user code, no frame objects are created at all. As a result, nearly all Python functions calls have sped up significantly.

> Most Python function calls now consume no C stack space, speeding them up.

\blank
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

# factorial -- [tail call optimization](https://en.wikipedia.org/wiki/Tail_call)

```
(define (fact-slow n)  ; TCO is disabled, so the call stack grows
  (if (zero? n)
      1
      (* n (fact-slow (sub1 n)))))


(fact-slow 5)
120
```
\newpage

# factorial -- tail call optimization

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

# stability -- ubuntu

![](ubuntu-versions.png)

# stability -- python interpreter

![](python-versions.png)

# stability -- PEP-719 interpreter releases

- 3.13.1: Tuesday, 2024-12-03
- 3.13.2: Tuesday, 2025-02-04
- 3.13.3: Tuesday, 2025-04-08
- 3.13.4: Tuesday, 2025-06-03
- 3.13.5: Wednesday, 2025-06-11
- 3.13.6: Wednesday, 2025-08-06
- 3.13.7: Thursday, 2025-08-14

[future](https://peps.python.org/pep-0719/#lifespan):

- 3.13.8: Tuesday, 2025-10-07
- 3.13.9: Tuesday, 2025-12-02
- 3.13.10: Tuesday, 2026-02-03 ...

# Makefile


```
measure: \
  $(REC)/py3.13 \
  $(REC)/py3.12 \
  $(REC)/py3.11 \
  $(REC)/py3.10 \
  $(REC)/py3.9 \
  $(REC)/py3.8 \

py%:
        mkdir $@
        cd $@ && uv venv --python $(shell basename $*)
        cd $@ && python $(DIR)/count.py
```
\newpage

# counting

```
def iterative_count(i: int, ceil: int) -> int:
    assert 0 == i, i  # Count up from zero, please.
    while i < ceil:
        i += 1
    return i


def recursive_count(i: int, ceil: int) -> int:
    if i < ceil:
        return int(recursive_count(i + 1, ceil))
    return i
```

# counting

```
def main() -> int:
    n = 30_000_000
    sys.setrecursionlimit(n + 10)

    if sys.version_info < (3, 11):
        n = 42_782  # max feasible value for interpreter 3.10.16
    if sys.version_info < (3, 10):  # noqa
        n = 72_289  # interpreters 3.8.20 & 3.9.23

    assert recursive_count(0, n) == n

    ver = sys.version.split()[0].ljust(10)
    print(end=f"{ver} {n:16,}\t")
    return n
```

# timing
\blank
```
Factorial 250000 found by #<procedure:fact-slow> in 29848 msec

Factorial 250000 found by #<procedure:fact>      in 10349 msec

```
\blank
![](https://asset.conrad.com/media10/isa/160267/c1/-/en/860048_BB_00_FB/image.jpg){height=4cm}

# image credits

\small

- https://en.wikipedia.org/wiki/Tower_of_Hanoi
  - AlejandroLinaresGarcia:
  - https://en.wikipedia.org/wiki/File:UniversumUNAM34.JPG
- https://xkcd.com/297 -- Randall Munroe
- https://asset.conrad.com/media10/isa/160267/c1/-/en/860048_BB_00_FB/image.jpg
- https://en.wikipedia.org/wiki/Ubuntu_version_history
  - https://upload.wikimedia.org/wikipedia/en/timeline/swfdceo7tl9n28j9pamsv083nwmv0l7.png
- https://en.wikipedia.org/wiki/History_of_Python
  - https://upload.wikimedia.org/wikipedia/en/timeline/3aeqr87p1hb7nohu4c5lnlkdiiypums.png
