
# process

Welcome to the dojo blackboard project!
We invite your contributions, big or small.
There's already a Hello World `greeting()`,
but perhaps you'd like to add a colorful version.
Or a map, or a Machine Learning analysis.

Most contributions should go through the PR process.
Not every project does things the same, so this will be a
learning  opportunity, to see alternate development approaches.
Just make up some new URL prefix using your initials or your feature name,
create a similarly named source folder, and put one or more `*.py` modules in it.
Feel free to make edits outside of that, hopefully small ones.
For example, you will likely need to add a web route to `main.py`
that will call your new feature function.
Start small, and build toward bigger features once you get the hang of things.

## new feature

1. Create a new [Issue](https://github.com/jhanley634/dojo-blackboard/issues). It can be a one liner: "do the thing", "add a HelloWorld page", whatever.
2. Create a new [Branch](https://github.com/jhanley634/dojo-blackboard/branches/all?query=99-new-branch) (look near the left margin, click on Main, then Find or create branch, then e.g. 9-hello-world if you created issue # 9), then click the suggested Create)
3. `git pull && git checkout 9-hello-world`, or whatever you named it
4. Edit / debug cycle, implement the feature, get it working, `git push` the feature branch up to GitHub.com.
5. Verify that `make lint` is clean (or at least that `ruff check` lints clean).
6. Submit a PR, which we will read and approve, so you can merge to the `main` branch where all can see it and run it.

## pull request

- Commit your edits, and verify the repo is clean by checking `git status`.
- Push your branch to GitHub.
- Visit the [repo](https://github.com/jhanley634/dojo-blackboard) and click the "Compare & pull request" button.
- Verify it is mergeable, and click the "Create pull request" button. Use `git pull main` to resolve any conflicts.
- Give Sourcery about two minutes to offer an automated first-pass rough review.
- Be the first reviewer. Read your own code in the "Files changed" tab, and see if that's what you intended.
Consider the Sourcery suggestions, feeling free to silently click "Resolve conversation" if / when you disagree.
- If new edits have occurred to you, make them in your branch, `make test`, and push them up to GitHub.
- Invite reviewers, such as John, Peter, or other participants, to review your PR.
- One of two things will happen:
  - Your PR will be approved, and you can merge it in the web UI, perhaps incorporating suggestions.
  - The 24-hour timeout will expire, so it is auto-approved, and you can merge it as-is.
- Close the Issue that you opened. We are done with it, and also done with the now-deleted feature branch.
- Consider tidying up your local repo: `git checkout main`, `git fetch --prune`, and e.g. `git branch -D 9-hello-world`.
- Lather, rinse, repeat: Create a new Issue, a corresponding Branch, pull / check it out, and keep hacking.

While awaiting review, you can certainly continue to work on some other feature in a new branch.
