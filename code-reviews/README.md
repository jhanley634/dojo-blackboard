This folder is for members of the Hacker Dojo Python Meetup to share code for the group to review.
Drop any code you have in here and in one of our next sessions the group can do a code review
to practice code reviews and to help make it better Python code.

If it's a single Python file, just drop it here.
If it's more than one Python file, make a subfolder and put the files there.
To keep things organized, name your files with your name as a prefix, eg: `peter-sudoku.py`

The easy way:

1. Ask in the Hacker Dojo Discord [Python channel](https://discord.com/channels/698267668918173827/1111141001818537985) to be added to the repo if you're not already added.
2. Go to the [Github webpage](https://github.com/jhanley634/dojo-blackboard) for the Hacker Dojo Python group project repo
3. Go in the 'code-review' folder and click the 'Add file' button to upload your Python file

The better way:

Just about every software development job involves using `git` as part of the workflow.
You should practice it any chance you get and get comfortable using `git` for versioning and collaborating all of your work.
When you use it for everything you will be delighted to find you have access to every version of everything you've ever worked on permanently available to you.

1. On your local machine go to your favorite projects folder, eg: `cd Documents`.
2. Clone the Hacker Dojo Python group project repo from github to a local folder: Go to the [repo website](https://github.com/jhanley634/dojo-blackboard) and click the green CODE button to get the URL, then type `git clone <the URL>`, for example: `git clone git@github.com:jhanley634/dojo-blackboard.git`
3. cd to the new project folder: `cd dojo-blackboard`, and to the code-review folder: `cd code-review`
4. Add your Python file or make a new folder under code-review and add multiple Python files to it.
5. Check in your code and upload it:
- `git add -A`
- `git commit -m "Jane Hackersmith's code for review"`
- `git push origin main`

The best way:

Code is best understood in the context of the whole project it is a part of including unit tests and what code is calling your code. If you contribute code to the dojo-blackboard over in the src/ folder it will be part of a larger project and we can have a much better discussion about how it fits into that project. Look at the project, add to an existing feature or make a new webpage (URL route) for your own new feature.
