
# dojo-secrets repo

Secret API keys can be found here:
https://github.com/jhanley634/dojo-secrets/blob/main/api-keys.txt

Do _not_ store valuable secrets in that repository,
as it is accessible to diverse Python Meetup participants.
If missuse of a key could reveal other secrets or cause more than $20 of loss
before detection and revocation of the key, then it is too valuable to store here --
find some different aspect of the group project to collaboratively work on.
Bad things happen not just through malice, but also through ignorance and accident.
Mistakes will occur, since we're all learning here.
Don't be surprised by the inevitable.
Be prepared to rev a key if accidental high usage is observed.

# cloning

Visit the Dojo on a Tuesday night and speak with Peter or John about getting access.
There will be no anonymous access.
You don't need to supply a LinkedIn profile, but it is very helpful.
We will need to know your real name, your Discord handle, and your GitHub userid.

Once an invite has been emailed via your GitHub ID, accept it and clone the repo.
Notice that attempts to read the repo without suitable credentials will fail
with 404, as it isn't publicly available.
Two sets of personal credentials are relevant:

1. within a browser
2. within a git client, such as the Bash command "git clone"

# token

A personal access token (PAT) should be used to authenticate your git client.
This is a secret, so don't share it.
If you already have one, you can use it.

If not, visit https://github.com to create one.
The token should have "repo" scope.
Click on your profile picture in the upper right corner, then "Settings",
then "Developer settings", then "Personal access tokens".
Your choices will be

- fine-grained permissions, or
- classic token.

Choose the latter.
The fine-grained permissions are more secure, but more complex.
They _should_ work for this project, but we've not yet seen that work.
Feel free to try it, and let us know what works for you.

Having generated a token, immediately copy it into a text file in your home directory,
as it will only be shown once. If lost you can always re-roll a new token.

When copy-n-pasting the token into your git client,
notice that a valid token  will always start with `github_pat_`.
If you don't see that, you haven't copied the full token value.

# siblings

Clone the dojo-secrets repo somewhere convenient,
and then clone the dojo-blackboard repo at the same level.
An `ls` in the parent directory should show both repos.

Put another way, this word-count command should indicate
how many API keys are available:
```bash
cd dojo-blackboard && wc -l ../dojo-secrets/api-keys.txt
```

# install

With the pair of repos in place, you are ready for install:
```bash
cd dojo-blackboard
make install
```
That will create a venv virtual environment in your home directory,
and will pip install the project's dependencies.
The top-level ReadMe offers additional details.
