# vim-python-domain-knowledge (NOT USABLE YET - under development⚠️)

Vim plugin for *Python* written in *Python* that automates usual development actions using project specific knowledge

## Motivation

A really common action in the python development is using functions that are not in the same file. The process usually looks like this:

1. Start typing the name (probably forgot the exact name since is long and explicitly descriptive)
2. Jump to the top of the file looking at the imports
3. Remember the place where the function lives
4. Find the right place in the imports to put the new function import
5. Start typing by autosuggesting the name using the import location
6. Jump back to the place where you want to use the function and autocomlete it

The aim of this plugin is to automate this process by generating knowledge for your existing codebase and use it to autosuggest the function/class/constant you want to use at the moment of typing + suggest the right import and put it at the right place.


## Setup

### 1. Installation

1. *Vundle*

Place this in your `.vimrc`

```
Plugin 'HackSoftware/vim-python-domain-knowledge'
```

… then run the following in Vim:

```
:source %

PluginInstall
```

2. *Plug*

Place this in your `.vimrc`

```
Plug 'HackSoftware/vim-python-domain-knowledge'
```

… then run the following in Vim:

```
:source %

PlugInstall
```

3. *Pathogen*

Run the following in a terminal:

```
cd ~/.vim/bundle
git clone https://github.com/HackSoftware/vim-python-domain-knowledge.git
```

### 2. Setup for project

1. Go to the project's root folder (where is your PYTHONPATH)

```
cd /path/to/project
```

2. Open Vim and run:

```
:call PythonDomainKnowledgeCollectImports()
```

*NOTE:* It could take a few seconds until it parse the whole project's Abstract syntax tree and extract the need

3. Restart Vim

4. You're ready

## Usage

### 1. Global autocomplete


### 2. Automatic import filling

## Configuration

