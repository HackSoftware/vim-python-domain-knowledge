# vim-python-domain-knowledge (NOT USABLE YET - under development⚠️)

Vim plugin for *Python* written in *Python* that automates usual development actions using project specific knowledge


## Documentation

* [Overview](#Overview)
* [Getting Started](#getting-started)
    * [Installation](#installation)
        - [Vundle](#vundle)
        - [Plug](#plug)
        - [Pathogen](#pathogen)
    * [Setup for a project](#setup-for-a-project)
* [Usage](#usage)
    * [Global autocomplete](#global-autocomplete)
    * [Automatic import filling](#automatic-import-filling)
* [Motivation](#motivation)


## Overview


Quick demo:
TODO: Gid needed

## Getting Started

### Installation

#### Vundle

Place this in your `.vimrc`

```
Plugin 'HackSoftware/vim-python-domain-knowledge'
```

… then run the following in Vim:

```
:source %

PluginInstall
```

#### Plug

Place this in your `.vimrc`

```
Plug 'HackSoftware/vim-python-domain-knowledge'
```

… then run the following in Vim:

```
:source %

PlugInstall
```

#### Pathogen

Run the following in a terminal:

```
cd ~/.vim/bundle
git clone https://github.com/HackSoftware/vim-python-domain-knowledge.git
```

*IMPORTANT NOTE:* The only external dependency of this plugin is SQLite3 (https://www.sqlite.org/index.html). Make sure you have it installed on your operating system :)

### Setup for a project

*NOTE:* this should be done only once for a project

#### Go to the project root folder

```
cd /path/to/project
```

#### Open Vim and run:

```
:call PythonDomainKnowledgeCollectImports()
```

*NOTE:* It could take a few seconds until it parse the whole project's Abstract syntax tree and extract the need. If everything is successfull you should see `.vim_domain_knowledge/` folder inside you project

#### Restart Vim (This is necessary since the plugin is setting up custom autocomplete function)

#### Add this to `.gitignore` (optionally)

```
.vim_domain_knowledge/

```

#### Enjoy

![Setup demo](./readme_media/setup_demo.gif "Setup demo")

## Configuration

```
" To map your shortcut for autofilling import for the word under the cursor
nnoremap <your_custom_mapping> :call PythonDomainKnowledgeFillImport()<CR>
```

Sample configuration:

```
" This will autofill the import for the word under the cursor when you press F9 key (in normal mode) :)
nnoremap <F9> :call PythonDomainKnowledgeFillImport()<CR>
```

## Usage

### Global autocomplete

Start typing and press `Ctrl + X` and then `Ctrl + U` (while in insert mode)
NOTE: You can remap this ^ . It's the default vim shortcut for autocomplete from custom `completefunc`

![Autocomplete demo](./readme_media/auto_complete_demo.gif "Autocomplete demo")

### Automatic import filling

Write the full name of the function/class you want to use. Then in *normal mode* run:

```
:call PythonDomainKnowledgeFillImport()<CR>
```

(or a keybinding for this)

![Import autofil demo](./readme_media/fill_imports_demo.gif "Autofil import demo 1")

![Import autofil demo](./readme_media/fill_imports_demo_2.gif "Autofil import demo 1")


## Motivation

A really common action in the python development is using functions that are not in the same file. The process usually looks like this:

1. Start typing the name (probably forgot the exact name since is long and explicitly descriptive)
2. Jump to the top of the file looking at the imports
3. Remember the place where the function lives
4. Find the right place in the imports to put the new function import
5. Start typing by autosuggesting the name using the import location
6. Jump back to the place where you want to use the function and autocomlete it

The aim of this plugin is to automate this process by generating knowledge for your existing codebase and use it to autosuggest the function/class/constant you want to use at the moment of typing + suggest the right import and put it at the right place.
