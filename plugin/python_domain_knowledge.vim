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
from vim_python_domain_knowledge.main import setup

try:
    print('What until plugin is ready...')
    setup()
    print('Done :)')
except Exception as exc:
    print('Error while setting up PythonDomainKnowledge')
    print(exc)
    pass
endOfPython
endfunction

function! PythonDomainKnowledgeRefreshFile()
python3 << endOfPython
from vim_python_domain_knowledge.main import refresh_from_file

try:
    refresh_from_file()
except Exception:
    pass
endOfPython
call SetupPythonDomainKnowledgeAutoComplete()
endfunction

function! PythonDomainKnowledgeFillImport()
python3 << endOfPython
from vim_python_domain_knowledge.main import fill_import

try:
    fill_import()
except Exception:
    pass
endOfPython
endfunction

function! SetupPythonDomainKnowledgeAutoComplete()
python3 << endOfPython
import vim
from vim_python_domain_knowledge.main import get_autocompletions_options_str


try:
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
except Exception:
    pass
endOfPython
endfunction

fun! PythonDomainKnowledgeFilterClose(bufnr)
  wincmd p
  execute "bwipe" a:bufnr
  redraw
  echo "\r"
  return []
endf

fun! PythonDomainKnowledgeSearchFunc(input, prompt) abort
 let l:prompt = a:prompt . '>'
 let l:filter = ""
 let l:undoseq = []
 botright 10new +setlocal\ buftype=nofile\ bufhidden=wipe\
   \ nobuflisted\ nonumber\ norelativenumber\ noswapfile\ nowrap\
   \ foldmethod=manual\ nofoldenable\ modifiable\ noreadonly
 let l:cur_buf = bufnr('%')
 if type(a:input) ==# v:t_string
   let l:input = systemlist(a:input)
   call setline(1, l:input)
 else " Assume List
   call setline(1, a:input)
 endif
 setlocal cursorline
 redraw
 echo l:prompt . " "
 while 1
   let l:error = 0 " Set to 1 when pattern is invalid
   try
     let ch = getchar()
   catch /^Vim:Interrupt$/  " CTRL-C
     return PythonDomainKnowledgeFilterClose(l:cur_buf)
   endtry
   if ch ==# "\<bs>" " Backspace
     let l:filter = l:filter[:-2]
     let l:undo = empty(l:undoseq) ? 0 : remove(l:undoseq, -1)
     if l:undo
       silent norm u
     endif
   elseif ch >=# 0x20 " Printable character
     let l:filter .= nr2char(ch)
     let l:seq_old = get(undotree(), 'seq_cur', 0)
     try " Ignore invalid regexps
       execute 'silent keepp g!:\m' . escape(l:filter, '~\[:') . ':norm "_dd'
     catch /^Vim\%((\a\+)\)\=:E/
       let l:error = 1
     endtry
     let l:seq_new = get(undotree(), 'seq_cur', 0)
     " seq_new != seq_old iff the buffer has changed
     call add(l:undoseq, l:seq_new != l:seq_old)
   elseif ch ==# 0x1B " Escape
     return PythonDomainKnowledgeFilterClose(l:cur_buf)
   elseif ch ==# 0x0D " Enter
     let l:result = empty(getline('.')) ? [] : [getline('.')]
     call PythonDomainKnowledgeFilterClose(l:cur_buf)
     return l:result
   elseif ch ==# 0x0C " CTRL-L (clear)
     call setline(1, type(a:input) ==# v:t_string ? l:input : a:input)
     let l:undoseq = []
     let l:filter = ""
     redraw
   elseif ch ==# 0x0B " CTRL-K
     norm k
   elseif ch ==# 0x0A " CTRL-J
     norm j
   endif
   redraw
   echo (l:error ? "[Invalid pattern] " : "").l:prompt l:filter
 endwhile
endf

call SetupPythonDomainKnowledgeAutoComplete()

function! PythonDomainKnowledgeSearch()
python3 << endOfPython
import vim
from vim_python_domain_knowledge.main import (
    get_search_options_str,
    navigate_to_file_by_search_obj_id,
)

try:
    search_options_str = get_search_options_str()

    search_function_trigger = f"""
    let python_domain_knowledge_search_options = {search_options_str}
    let python_domain_knowledge_search_items = PythonDomainKnowledgeSearchFunc(python_domain_knowledge_search_options, '>')
    let g:python_domain_knowledge_search_result = empty(python_domain_knowledge_search_items) ? v:null : split(python_domain_knowledge_search_items[0], '|')[1]
    """
    vim.command(search_function_trigger)

    obj_id = vim.eval('g:python_domain_knowledge_search_result')

    if obj_id:
        navigate_to_file_by_search_obj_id(obj_id=obj_id)

except Exception as exc:
    pass
endOfPython
endfunction
