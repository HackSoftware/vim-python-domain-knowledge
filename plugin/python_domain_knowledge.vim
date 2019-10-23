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
