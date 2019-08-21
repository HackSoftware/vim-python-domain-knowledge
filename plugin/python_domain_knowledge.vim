" -------------------
" Add to path
" -------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:p:h")'))

" -------------------
"  Functions
" -------------------

function! PythonDomainKnownledge()
python3 << endOfPython
from src.main import hello_world

hello_world()
endOfPython
endfunction
