
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


\newpage
# image credits

- https://en.wikipedia.org/wiki/Tower_of_Hanoi
  - AlejandroLinaresGarcia: https://en.wikipedia.org/wiki/File:UniversumUNAM34.JPG
