# vim-python-domain-knowledge (under development⚠️)

Vim plugin written in Python that automates usual development actions using project specific knowledge

## Motivation

A really common action in the python development is using functions that are not in the same file. The process usually looks like this:

1. Start typing the name (probably forgot the exact name since is long and explicitly descriptive)
2. Jump to the top of the file looking at the imports
3. Remember the place where the function lives
4. Find the right place in the imports to put the new function import
5. Start typing by autosuggesting the name using the import location
6. Jump back to the place where you want to use the function and autocomlete it

The aim of this plugin is to automate this process by generating knowledge for your existing codebase and use it to autosuggest the function/class/constant you want to use at the moment of typing + suggest the right import and put it at the right place.

## Version 1.0.0 roadmap:

- ~Ability to autosuggest an import for the function/class/variable under the cursor using a statistics over the existing imports for this function accross the project~
- ~Automatically suggest and add function/class/variable import at the right place in the file~
- ~Global fuzzy match autocomplete using the "visible" classes, functions and variables (for all python files in the project) ordered by frequency of usage accross the project~
- Add tests


## API for 1.0.0

- ~Vim function that triggers refresh of the project knowledge~
- ~Vim function that triggers suggestion of import source and auto add the import on confirmation~
- ~Vim function that opens dropdown for the word under the cursor suggesting the `N most possible classes/functions/variables with their sources` in the project that fuzzy matches the pattern (+ autoadd the import at the right place)~

## Technical requirements for 1.0.0:

- ~Written in python~
- Asynchronous work (using Vim 8 API)
- ~Use SQLite for keeping project knowledge~
- ~Store all of the project specific knowledge in a folder in the project (`.vim-python-knowledge/` for exapmle) in SQLite database~
