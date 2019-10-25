" -------------------
" Add to path
" -------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:p:h")'))

" -------------------
"  Functions
" -------------------

" First of all - setup autocomplete dictionary path
set complete+=k
set dictionary+=.vim_domain_knowledge/vim_domain_knowledge_dictionary.txt
autocmd BufWrite *.py :call PythonDomainKnowledgeRefreshFile()


function! PythonDomainKnowledgeCollectImports()
python3 << endOfPython
from src.main import setup

setup()
endOfPython
endfunction

function! PythonDomainKnowledgeRefreshFile()
python3 << endOfPython
from src.main import refresh_from_file

refresh_from_file()
endOfPython
endfunction

function! PythonDomainKnowledgeFillImport()
python3 << endOfPython
from src.main import fill_import

fill_import()
endOfPython
endfunction

function! SetupAutoComplete()
python3 << endOfPython
import vim
from src.main import get_autocompletions_options_func

matches = get_autocompletions_options_func()
matches_str = 'let l:data = [' + ','.join([f'["{name}", "{module}"]' for name, module in matches]) + ']'

function = ('''
    fun! MyComplete()
        " The data. In this example it's static, but you could read it from a file,
        " get it from a command, etc.
        '''
        f'{matches_str}'
        '''

        " Locate the start of the word and store the text we want to match in l:base
        let l:line = getline('.')
        let l:start = col('.') - 1
        while l:start > 0 && l:line[l:start - 1] =~ '\\a'
            let l:start -= 1
        endwhile
        let l:base = l:line[l:start : col('.')-1]

        " Record what matches − we pass this to complete() later
        let l:res = []
        "Add empty result
        call add(l:res, {
            \ 'icase': 1,
            \ 'word': l:base,
            \ 'abbr': '',
            \ 'menu': '',
            \ 'info': '',
            \ 'empty': '',
            \ 'dup': ''
        \ })

        " Find matches
        for m in l:data
            " Check if it matches what we're trying to complete; in this case we
            " want to match against the start of both the first and second list
            " entries (i.e. the name and email address)
            if l:m[0] !~? '^' . l:base && l:m[1] !~? '^' . l:base
                " Doesn't match
                continue
            endif

            call add(l:res, {
                \ 'icase': 1,
                \ 'word': l:m[0],
                \ 'abbr': '',
                \ 'menu': l:m[1],
                \ 'info': '',
                \ 'empty': '',
                \ 'dup': ''
            \ })
        endfor

        " Now call the complete() function
        call complete(l:start + 1, l:res)
        return ''
    endfun

    inoremap <C-x><C-m> <C-r>=MyComplete()<CR>
'''
)
vim.command(function)
endOfPython
endfunction
call SetupAutoComplete()
