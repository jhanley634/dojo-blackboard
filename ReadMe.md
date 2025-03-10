
[![Coverage Status](https://coveralls.io/repos/github/jhanley634/dojo-blackboard/badge.svg?branch=main)](https://coveralls.io/github/jhanley634/dojo-blackboard?branch=main)

This repo supports the [Hacker Dojo](https://www.hackerdojo.com) Blackboard project,
developed by the local python [community](https://www.meetup.com/hackerdojo/events).
Come visit us at the Dojo on Tuesday evenings at 6:30pm to participate.

Begin by following these setup instructions.
```bash
make install
make run
```
That will create a venv virtual environment in your home directory,
and run the app within that environment.
Now it's available to your browser using a localhost URL.
Another two targets you might care to try out are `make lint test`.

Next step is to jump into the development [process](docs/).

----

This codebase is frequently tested under [linux](https://ubuntu.com) and macOS.
It is designed to work on all posix systems, including windows WSL 2.
Please [report](https://github.com/jhanley634/dojo-blackboard/issues)
any rough edges you may encounter.

----

Note that `make` uses this setting:
```bash
PYTHONPATH := src:.
```
When running commands outside of `make`, you may need to set this env var explicitly.

Within the PyCharm IDE you will want to visit Settings ->
Project: dojo-blackboard -> Project Structure, and mark the `src` directory as Sources.
