" -------------------
" Add to path
" -------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:p:h")'))

" -------------------
"  Functions
" -------------------

autocmd BufWrite *.py :call PythonDomainKnowledgeRefreshFile()
" To not prefill the first option from the autocomplete
set completeopt=menuone,longest,preview

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
call SetupPythonDomainKnowledgeAutoComplete()
endfunction

function! PythonDomainKnowledgeFillImport()
python3 << endOfPython
from src.main import fill_import

fill_import()
endOfPython
endfunction

function! SetupPythonDomainKnowledgeAutoComplete()
python3 << endOfPython
import vim
from src.main import get_autocompletions_options_str

matches_str = get_autocompletions_options_str()

complete_func = (
'''
	fun! PythonDomainKnowledgeCompleteFunc(findstart, base)
      if a:findstart
        " locate the start of the word
        let line = getline('.')
        let start = col('.') - 1
        while start > 0 && line[start - 1] =~ '\\a'
          let start -= 1
        endwhile
        return start
      else
        '''
        f'{matches_str}'
        '''
        let res = []
        for m in l:data
          if m['word'] =~ '^' . a:base
            call add(l:res, m)
          endif
        endfor
        return res
      endif
	endfun
    autocmd FileType python setlocal completefunc=PythonDomainKnowledgeCompleteFunc
'''
)

vim.command(complete_func)
endOfPython
endfunction

call SetupPythonDomainKnowledgeAutoComplete()
