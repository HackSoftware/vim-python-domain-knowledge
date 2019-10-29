from vim_python_domain_knowledge.common.vim import Vim

CURRENT_DIRECTORY = Vim.eval("getcwd()")
KNOWLEDGE_DIRECTORY = f'{CURRENT_DIRECTORY}/.vim_domain_knowledge/'
DB_NAME = 'vim_domain_knowledge.db'
DB_PATH = f'{KNOWLEDGE_DIRECTORY}{DB_NAME}'
