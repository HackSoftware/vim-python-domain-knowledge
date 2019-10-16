" -------------------
" Add to path
" -------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:p:h")'))

" -------------------
"  Functions
" -------------------
" TODO: This is temporary
set complete+=k
set dictionary+=.vim_domain_knowledge/vim_domain_knowledge_dictionary.txt

function! PythonDomainKnowledgeCollectImports()
python3 << endOfPython
from src.main import setup

setup()
endOfPython
" TODO: Ideally get this from the python settings
set complete+=k
set dictionary+=.vim_domain_knowledge/vim_domain_knowledge_dictionary.txt
endfunction

function! PythonDomainKnowledgeFillImport()
python3 << endOfPython
from src.main import fill_import

fill_import()
endOfPython
endfunction
