# Lesson 1 Assignment 1 - Advanced Unit Testing

### Minor Details:
* Code Poet: Anthony McKeever
* Start Date: 10/16/2019
* End Date: 10/18/2019
* Redmine Issue: SchoolOps-11

## Application Run Instructions

1. Navigate to the `lesson_1/assignment_1` folder.
    * Windows CMD: `cd students\anthony_mckeever\lesson_1\assignment_1`
    * Unix/Linux based: `cd students/anthony_mckeever/lesson_1/assignment_1`
1. Run `main.py` as a module
    * `python -m inventory_management.main`

## Test Execution Instructions

### Unit Tests With Coverage

1. Navigate to the `lesson_1/assignment_1` folder.
    * Windows CMD: `cd students\anthony_mckeever\lesson_1\assignment_1`
    * Unix/Linux based: `cd students/anthony_mckeever/lesson_1/assignment_1`
1. Execute the unit tests command through Coverage.py
    * `coverage run --source=inventory_management -m unittest test_unit -v`
1. Execute the command to create a report
    * `coverage html`
1. Open the `htmlcov/index.html` file to view the report.

### Unit Tests no Coverage

1. Navigate to the `lesson_1/assignment_1` folder.
    * Windows CMD: `cd students\anthony_mckeever\lesson_1\assignment_1`
    * Unix/Linux based: `cd students/anthony_mckeever/lesson_1/assignment_1`
1. Executeh the Unit Test command in python:
    * `python -m unittest test_unit.py`

### Integration Tests

1. Navigate to the `lesson_1/assignment_1` folder.
    * Windows CMD: `cd students\anthony_mckeever\lesson_1\assignment_1`
    * Unix/Linux based: `cd students/anthony_mckeever/lesson_1/assignment_1`
1. Executeh the Test command in python:
    * `python -m unittest test_integration.py`