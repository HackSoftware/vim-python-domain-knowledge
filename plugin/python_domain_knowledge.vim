" -------------------
" Add to path
" -------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:p:h")'))

" -------------------
"  Functions
" -------------------

function! PythonDomainKnowledge()
python3 << endOfPython
from src.main import main

main()
endOfPython
endfunction
