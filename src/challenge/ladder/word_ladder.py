"""
Challenge: Write a program to find the shortest path to change one
word into another. It takes a word_list, a start_word and a target_word.
From the start_word each "turn" you can change just one letter of the
word to form another word. The new word must be a valid word in the
word_list. Find the shortest list of words that takes you from the
start_word to the target_word. Return the list of words, or [] if
there is no way to change the start_word into the target_word.

Example: find_word_path(start_word="hit", target_word="cog", word_list=dictionary)
 ->  ["hit", "hot","dot","dog","lot","log","cog"]
ControlAltPete
"""

from pprint import pp
from string import ascii_lowercase
from time import time

from networkx import Graph, NetworkXNoPath, shortest_path

assert 26 == len(ascii_lowercase)

t0 = [0.0]


def tic() -> None:
    t0[0] = time()


def toc(thresh: float = 0.005) -> float:
    elapsed = time() - t0[0]
    if elapsed > thresh:
        print(f" {elapsed:.6f} seconds")
    return elapsed


def find_word_path(
    start_word: str,
    target: str,
    lexicon: set[str],
    *,
    verbose: bool = False,
) -> list[str]:
    if start_word == target:
        return [start_word]
    if target not in lexicon:
        return []  # It's impossible to reach a non-existent word.

    desired_length = len(target)
    lexicon = {word for word in lexicon if len(word) == desired_length}
    if verbose:
        print("\n", desired_length, len(lexicon))

    g = Graph()  # a bipartite graph, from words like "cat" to wildcards like "c.t"
    for word in sorted(lexicon):
        w = bytearray(word, "utf8")
        for i in range(len(word)):
            w[i] = ord(".")  # a Kleene regex wildcard character
            wildcard = w.decode()
            g.add_edge(word, wildcard)
            w[i] = ord(word[i])

    if verbose:
        _display_graph_details(g)

    try:
        tic()
        path = shortest_path(g, source=start_word, target=target)
        toc()  # We typically observe sub-millisecond performance.
        return [word for word in path if "." not in word]  # Elide the wildcards.
    except NetworkXNoPath:
        return []


def _display_graph_details(g: Graph) -> None:
    print("\n", g.number_of_edges(), "edges, and", g.number_of_nodes(), "nodes")
    details = []
    degree = g.degree
    assert not isinstance(degree, int)
    for word, d in degree:
        if "." in word and d > 5:
            details.append((d, word, "  ".join(g.neighbors(word))))
    pp(sorted(details))
