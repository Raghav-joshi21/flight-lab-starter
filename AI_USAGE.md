# AI Usage Disclosure

<!--
Fill in this file before you submit. Submissions without it are not graded.
If you used no AI tools, delete everything below and write only:
No AI tools were used.
-->

## Tools used

- Chat gpt used 

## Conversation links

- Link 1: https://chatgpt.com/share/6b05b4a2-f61c-83eb-b97b-28ef95c30993

## What I used them for

- e.g. I tried to ask ChatGPT about the assignment first that what I actually need to do the assignment then I asked that from where should I start? He answered me that you should start from this file and then I started to write code and whenever i stuck I ask ChatGPT via error code or screenshot, and then he answered me and suggested me changes in some chunk, of course which I need to implement in my codebase base and that's how I use ChatGPT for this assignment.

## Which parts of the code were AI-generated or substantially AI-assisted 
// i asked this to ai because he knows my chat history
1. validator.py

Understanding load_airports() implementation in Python using sets, file reading and whitespace handling.
Define helper functions to parse prices (_parse_price()) and datetimes (parse_datetime())
11 flight validation checks to be understood and implemented in the required order.
Learn about airport validation, check airport code format and check if it exists in the airport list.
Debugging a Python Variable Scope Error with DATETIME_FORMAT
Understanding strict datetime format and finite price validation.

2. csv_loader.py

Knowing what to import from validator.py
The parse_files() workflow is designed to read CSV files and separate the valid rows from the invalid ones.
Learning of duplicate detection with a set of (flight_id, departure_datetime) pairs.
Variable usage and error collection logic. Debugging dictionary key errors.

3. query.py
Permitted query keys and invalid query detection.
Designing the _matches() function to apply AND conditions for filtering flights.
Learn how to match exactly, compare datetimes and filter by minimum and maximum price.
Sorting, sorted(), lambda functions, sort_by and order.
Debugging a NameError from an undefined sorting key.

## Key prompts

Here is the assignment. Please help me understand it. "Don't give me the whole code first, tell me the key requirements so that I can write it by myself." "I have written the load_airports function. Do we need to write any helper functions to interpret the data? If so, what will they do?
I have made the _matches() function. Inside it what conditions do I need to check based on the requirements of the assignment?
More prompts for debugging and understanding :
I am getting this type of error. What is the concept of allowed keys in query.py? What is wrong here?
I am getting a NameError that key is not defined when I sort. Could you explain how to fix it ? "

## What I changed or verified myself
I wrote and implemented the Python functions myself, based on the requirements of the assignment and the guidance from ChatGPT.
I fixed the airport loading logic to save all valid airport codes in a set.
I have done the validation checks in the correct order and make sure that only the first validation error is returned.