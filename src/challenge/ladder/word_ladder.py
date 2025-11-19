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

from collections import deque
from string import ascii_lowercase

assert 26 == len(ascii_lowercase)


def find_word_path(start_word: str, target: str, lexicon: set[str]) -> list[str]:
    if start_word == target:
        return [start_word]

    if target not in lexicon:
        return []  # It's impossible to reach a non-existent word.

    lexicon = lexicon.copy()
    queue = deque([(start_word, [start_word])])

    while queue:
        current_word, path = queue.popleft()

        for i in range(len(current_word)):
            # Try changing each letter of the current word to every other letter.
            for c in ascii_lowercase:
                next_word = current_word[:i] + c + current_word[i + 1 :]

                if next_word == target:
                    return [*path, next_word]

                # Only continue with valid words that haven't been visited yet.
                if next_word in lexicon:
                    lexicon.remove(next_word)  # Mark that word as visited.
                    queue.append((next_word, [*path, next_word]))

    return []  # There's no solution.
