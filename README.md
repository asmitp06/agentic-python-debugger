# agentic-python-debugger

Temp text for testing:

the user would input a file and possible context regarding their files.
Then the file would go through an executer agent it runs the code, and see's if the code errors out. If there are testcases, it creates those, and runs it on each testcase
Then the file, the context, and output of the testcases go to the analyzer, which concretely points out a list of what errors there are, and where they are. If no errors, skip to 6
Then the fixer takes the code and list of errors and where they are to fix the code so that it works
This goes back to the executer (2), which then goes back the analyzer (3), which decides if the code works or not. If it doesn't, it goes back to the fixer (4). If it does, it goes to the critic
The critic looks to make sure the code is will written and well optimized, if it suceeds it goes to the user, if it fails it goes back to the fixer at 4.
 
Executer(code, context)  = CodeRunner(code, TestCaseMaker(code, context)) --> JSON of testcases, and type of error, exact errormessage/output
Analyzer(code, context, ExecuterJSON) --> bad it gives json of what lines in the code there are errors, what the errors are, and ideas on how to fix, as well as the a boolean for good or bad
Fixer(code, AnalyzerJSON) --> fixed code
Critic(fixed code, context) --> boolean for is it good and optimized as well as a JSON of what lines are badly written, need more comments, or other code review information for fixer
