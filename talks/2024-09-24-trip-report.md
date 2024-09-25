
---
title: PyBay trip report
subtitle: and Five Rules
author: John Hanley
date: 23\textsuperscript{rd} September 2024
geometry: paperwidth=8in, paperheight=6in
header-includes:
    - \usepackage{setspace}
    - \onehalfspacing
---
[//]: # ( Copyright 2024 John Hanley. MIT Licensed. )

\newcommand{\blank}{\vspace{4mm}\vfill}
\Large
\newpage
\hrule
\blank

Agenda:

\vskip 11mm

- Five Rules
- PyBay trip report
- Peter: [SSE](https://en.wikipedia.org/wiki/Server-sent_events) for [HTMX](https://en.wikipedia.org/wiki/Htmx)
- constraints: OR / [SAT](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem#3-satisfiability) solvers
  - shortest path
  - soduko

\blank
\hrule

\newpage

[CACM](https://dl.acm.org/toc/cacm/2024/67/8)

[PHK: FOSS and Other Market Failures](https://dl.acm.org/doi/10.1145/3670242):
\textrm{\large "I Come Not to Praise FOSS."}

[GNN, d.b.a. Kode Vicious](https://dl.acm.org/doi/10.1145/3665518)

[Craig Partridge](https://en.wikipedia.org/wiki/Craig_Partridge)

> ... you cite one of my favorite books on the topic of good software engineering,
> [The Practice of Programming](https://en.wikipedia.org/wiki/The_Practice_of_Programming)
> by Kernighan and Pike, a classic I read when it came out more than 20 years ago.


\newpage
# Five Rules

\blank

1. Code that appears in [more than one place](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) should be a function.
2. A function should be less than 30 lines long.
3. A function should have at most [three levels](https://en.wikipedia.org/wiki/Cyclomatic_complexity) of conditional control.
4. Create a function when it improves readability.
   - Don’t comment bad code, rewrite it. Kernighan and Pike.
5. [Do one thing.](https://en.wikipedia.org/wiki/Single-responsibility_principle)

\blank
\hyphenation{persistent}

# PyBay 2024 trip report

SF, Mission Bay, \textrm{\large https://pybay.org/attending/schedule }

1. From Pandas to Polars: Upgrading Your Data Workflow; Matt Harrison.
2. The Five Demons of Python Packaging That Fuel Our Persistent Nightmare; Peter Wang.
3. Automate Your City Data With Python; [Philip James](https://www.youtube.com/watch?v=MtWzNnZvQ6w).
4. F-Strings!; Mariatta Wijaya. `f"{name=}"`, 'nuff said.
5. Master Python typing with Python-Type-Challenges; [Laike9m](https://github.com/laike9m/Python-Type-Challenges).
6. PyTest, The Improv Way; Joshua Grant. [\textrm{\large playwright.dev}](https://playwright.dev/docs/writing-tests\#actions)
7. Edges of Python: Three Radical Python Hacks for Fun and Profit; Elvis Pranskevichus. [\textrm{\large HAMT immutables}](https://pypi.org/project/immutables)
8. [Pyre](https://pypi.org/project/pyre-check), Lints, Codemods, Code Quality, and You; Maggie Moss.

# OR, constraints

\blank

Would you like to play a game?

\blank

https://www.nytimes.com/games/connections

\blank
