<h2 align="left" style="font-weight:bold">🌱 Getting Started </h2>

### Setup the repository to your local environment.

**1.** `Fork` the repository: Creates a replica of repository to your local environment.

**2.** Local Machine setup:- 
 ```git
 git config --global user.name "GITHUB_USER_NAME"
 ```
Enter your github user name instead of **GITHUB_USER_NAME**.

 ```git
 git config --global user.email "email@gmail.com"
 ```
Enter your email linked to github account instead of **email@gmail.com**.

```git
git config -l
```

**3.** Clone the repository - 

Downloads all repo files to your machine, using:-
```git
git clone https://github.com/YOUR-USERNAME/newsXplorer
```
   - Enter user_name
   - Press ok
   - Enter **access token** instead of password
   - Press ok

**4.** Set working directory to the root directory of the project.
```sh
cd newsXplorer/
```

**5.** Install prerequisite:-

```bash
pip install -r requriments.txt
```
  - Run the app:-
```bash
python main.py
```

  - And, open [127.0.0.1](127.0.0.1)


**6.** Cheers! 🎉 Now the repository has been setup in your local machine. Open your editor and start coding, & for visual studio code, run command in terminal:-
```sh
code .
```

**7.** Add a reference(remote) to the original repository.
```
git remote add upstream https://github.com/devstrons/newsXplorer.git
```

**8.** Perform your desired changes to the code base.


**9.** Track your changes ✅

```
git add . 
```

**10.** Commit your changes.

```
git commit -m "Relevant message"
```

**11.** Check for your changes.

```
git status
```

**12.** Push the committed changes in your feature branch to your remote repo.

```
git push -u origin <your_branch_name>
```

**13.** To create a pull request, click on `compare and pull requests`. Please ensure you compare your feature branch to the desired branch of the repo you are suppose to make a PR to.

**14.** Add appropriate title and description to your pull request explaining your changes and efforts done.

**15.** Click on `Create Pull Request`.

**16.** Voila ❗️ You have made a PR to the website 💥 . Sit back patiently and relax while the project maintainers review your PR. Please understand, at timesthe time taken to review a PR can vary from a few hours to a few days.

**NOTE:-**
- If there is no tracking information for the current branch. Please specify which branch you want to merge with. See git-pull(1) for details.
```sh
git pull
```
- If you wish to set tracking information for this branch you can do so with:
```sh
git branch --set-upstream-to=/ main
```
- Check the remotes for this repository.

```
git remote -v
```
