# Anthony McKeever's SP_Python220B_2019 Course Materials

*“There’s nothing wrong with being frustrated by defeat, but when you have fun making something, it really shows in the final product. That’s the power of positivity at work.”* – Yagami Kou (New Game!)

## Purpose

The purpose of this folder is to contain Anthony McKeever's course work based on the materials of the UW Python Certificate Program's Advanced Programming in Python (PY220B) course.

## Structure

Each course lesson will contain its own folder.  The folders will use the naming convesion `lesson_X` where `X` will be the lesson number.  For example, anything for Lesson 1 will be in the `lesson_1` directory.  Each assignment will use the naming convesion `assignment_Y` where `Y` will be the assignment number.  Each assignment may have several child directories that align to the names outlined in the assignment.

### Source Map:
```
<students directory>
    `-- anthony_mckeever                    <Root folder of Anthony's course materials>
        `-- lesson_1                        <Content for Lesson 1>
            |-- activity_1                  <Content for Lesson 1 Activity 1 - Automated Testing>
            `-- lesson_1                    <Content for Lesson 1 Assignment 1 - HP Norton Project>
                |-- inventory_management    <Inventory management system (initially copied from Lessons directory in repo root)>
                `-- tests                   <Inventory management system tests (initially copied from Lessons directory in repo root)>
```

## Branching

Branching will be done for each lesson so as to not polute master with in development and potentially buggy code.  Each branch go through a self code review to ensure quality and completeness before merging into `Snip3rM00n/SP_Python220B_2019/Master`.  After all items for the lesson or activity are in `Snip3rM00n/SP_Python220B_2019/Master` they will then be sent as a PR to Upstream (`UWPCE-PythonCert-ClassReops/SP_Python220B_2019`).

### Self Review Process

Before being merged into fork master (`Snip3rM00n/SP_Python220B_2019/Master`) each branch will go through a self review process to ensure the following criteria are met:
* Assignment Completeness
    * Assignment code meets all the requirements and specs that have been outlined in the assignment.
* Accuracy and Consistency of White Space
    * A must for Pythonic code.
* Refactoring and/or Removal of Unnecessary Code
    * A clean application is a happy application.
    * Applications are like a good math problem: reduce.
* PEP8 Alignment
* Code documentation
    * Doc Strings
    * Code comments on complex code
    * Code sheet headers
* Code coverage (local machine)
    * Ensure code is covered as close to 100% by unit tests as possible.
        * Excluding the "name is main" block if applicable.

Once a branch meets the criteria above it can be *squashed* to Master and a Pull Request can be made to merge to the upstream remote master and the assignment can be submitted.