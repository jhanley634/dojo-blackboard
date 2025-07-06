
---
title: LLMs and NYT Connections
subtitle: know your tools
author: John Hanley
date: 8\textsuperscript{th} July 2025
geometry: paperwidth=8in, paperheight=6in, left=2.2cm
header-includes:
    - \usepackage{setspace}
    - \onehalfspacing
    - \usepackage{graphicx}
    - \pagestyle{empty}
---
[//]: # ( Copyright 2025 John Hanley. MIT Licensed. )

\newcommand{\blank}{\vspace{4mm}\vfill}
\thispagestyle{empty}
\Large
\newpage

# You're doing it wrong

Often we celebrate triumphs.

"Do _this_ and it will work great!"

We can learn from the win.
And also from the "whoops!".
\blank

\hfil ![](https://evgmedia.com/wp-content/uploads/2013/07/bush_doing_it_wrong.jpg){height=3.2cm}


# publication bias

Failed experiments can teach things, as well.

\newpage

# share your experiences

\vfil

Tell us how you found better results, please.

\newpage

# know your tools

![](https://media.istockphoto.com/id/483859333/vector/open-toolbox-with-tools.jpg?s=612x612&w=0&k=20&c=y9GHkRi89jmH2dMafKYidVMMmuFJvO3iIFmLxzGtMzQ=){height=4.7cm}
\hfill
![](https://web.archive.org/web/20250706001708if_/https://toolsowner.com/wp-content/uploads/2023/08/What-Is-The-Difference-Between-Flathead-And-Phillips-Screwdriver-768x576.jpg){height=4.7cm}

- choose an appropriate datastructure
- .CSV, RDBMS
- Kafka, Redis
- 3SAT solvers (ORtools)
- symbolic algebra
- A* planners

\newpage

# SkyNet

\vfil
![](https://elchapuzasinformatico.com/wp-content/uploads/2023/02/Creador-ChatGPT-OpenAI-IA-Skynet.jpg){height=7cm}

# river crossing


On the left bank of a river we see

- a canoe
- 1 farmer
- 3 wolves
- 5 sheep

The two locations are the: left bank and the right bank.

The canoe can accommodate the farmer plus, at most, two animals.

If the farmer is at a location, no sheep will be eaten.
If sheep outnumber wolves at a location, no sheep will be eaten.
Otherwise wolves will eat sheep, for example if 1 wolf and 1 sheep are alone on a bank.

\newpage

The farmer makes a  sequence of moves to safely arrange for all animals to be on the right bank.
No sheep should be eaten by wolves.
After the final move we should see 3 wolves and 5 sheep in the right bank.
A "move" is a trip from left to right bank, or a trip from right to left bank.
What is the minimum number of moves he must make?
Verify that each move is valid, and that no sheep are eaten.

On the last line of your answer, display FINAL ANSWER, the number of moves, and the
text "I hope this final answer is correct."

## answers

\hyphenation{routinely}

Diverse, sub-optimal, and poor.
Conservation of matter was routinely violated.

# models

```bash
$ ollama list | awk '$3 > 6.0' | sort -n -k3
NAME                        ID              SIZE      MODIFIED
gemma3:12b                  f4031aab637d    8.1 GB    2 days ago
olmo2:13b                   6c279ebc980f    8.4 GB    2 days ago
deepseek-coder-v2:latest    63fb193b3a9b    8.9 GB    2 days ago
cogito:14b                  d0cac86a2347    9.0 GB    2 days ago
deepseek-r1:14b             c333b7232bdb    9.0 GB    3 weeks ago
phi4:latest                 ac896e5b8b34    9.1 GB    2 days ago
qwen3:14b                   bdbd181c33f2    9.3 GB    2 days ago
phi4-reasoning:latest       47e2630ccbcd    11 GB     3 weeks ago
devstral:latest             c4b2fa0c33d7    14 GB     3 weeks ago
magistral:latest            5dd7e640d9d9    14 GB     3 weeks ago
```

# platform

\blank

![](asset/2025-07-08/M4.png)

# simple problems

- How many R's in "strawberry" ?
- recent SCOTUS appointees
- related word pairs
- farmer moves wolves + sheep across river

\newpage

# recent SC justices

I'm interested in recent US supreme court appointments:
year appointed, age at appointment, party affiliation of president,
term number of president, name of president, name of justice.

Give just the last name of the president, and just the last name of the justice.
G. Bush was presidential term number 41, G. H. W. Bush was 43, Trump was 45 and again 47.
Only consider justices who ultimately were successfully confirmed by the Senate.

Present it in tabular form, with column headings of year, age, party, term, president, justice.
Choose one of {Dem., Rep.} for party.

Put it in reverse chronological order.
Be sure to list the 20 most recent appointments.

# related word pairs

Create a dozen pairs of related words, such as {taper, tapper}, where doubling the consonant changes the vowel sound. In the example it changes from long A to a short A sound.

Each word must be two or three syllables long.
Both words must have the identical ending.
So do not e.g. append an -ed or -ly or -ing suffix to alter a word.
