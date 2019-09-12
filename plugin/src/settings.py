import os
import vim

CURRENT_DIRECTORY = vim.eval("getcwd()")
KNOWLEDGE_DIRECTORY = f'{CURRENT_DIRECTORY}/.vim_domain_knowledge/'
DB_NAME = 'vim_domain_knowledge.db'
DB_PATH = f'{KNOWLEDGE_DIRECTORY}{DB_NAME}'
