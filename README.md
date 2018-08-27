# latexResearchDiary - A LaTeX-based and collaborative research diary

How often have you returned to an old task wondering what you were thinking the last time you worked on it? Did I really write this piece of code? How did I connect the DUT to the measurement equipment? What did I search for in Google when I found that interesting paper? What did I name that file? Where did I place that piece of paper with the magnificent derivation? Unfortunately, I am guilty of asking myself these and many other questions way too often. Yes, I tend to forget things. Even important things. Things which I am sure that the future me will remember, but he often disappoints me.

I am also guilty of being a happy LaTeX user. And friendly - to the future version of myself at least. Therefore, I decided to create the present LaTeX-based work diary to the forgetful future me. The diary resembles a good old lab journal, but it is hopefully also much more powerful while still being fairly simple to use. The focus should be on the work - not on managing a diary - because the current me hates bureaucracy.

Sure sure, that all sounds great and all, but how do you manage the diary in two years from now when it consists of 1000 pages? What about in 10 years? Can you write confidential information in the diary and still share your work with an external partner? Yes, you can! Thanks to a tagging system, the diary can be build conditionally on these tags or on the time. If I remember it, I will say much more about this later.

The work diary can also be used as a collaborative tool for multiple forgetful people working on the same project. When used in this way, the diary is a project diary which serves as the documentation of the project.

## How to get started
Please start by reading [the documentation](latexResearchDiary/master.pdf) which has a nice introductory example. To start your own diary, please follow the following steps.
1. Create a folder named, e.g., 'myDiary' somewhere in your filesystem
2. Copy the entire content of the latexResearchDiary repos to that folder
3. Delete all files in the folder 'buildFiles', all files in the folder 'entries', and the 'diaryDatabase.db' file in the 'database' folder.
4. Optionally, you can also delete the folder named 'tests' which contains all files used for the unit testing.

## Scope and limitations
I made this LaTeX-based research diary back in 2014 and has used it ever since. Unfortunately, I am now quite busy with many other things which means that I do not have time to refine it anymore. I have therefore decided to move everything to Github so that people with more time and skills than me can keep developing it.

