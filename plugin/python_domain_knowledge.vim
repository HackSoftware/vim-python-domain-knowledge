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
        " find months matching with "a:base"
        let res = []
        '''
        f'{matches_str}'
        '''
        for m in l:data
          if m['word'] =~ '^' . a:base
            call add(l:res, m)
          endif
        endfor
        return res
      endif
	endfun
	set completefunc=PythonDomainKnowledgeCompleteFunc
'''
)

vim.command(complete_func)
endOfPython
endfunction

call SetupAutoComplete()
