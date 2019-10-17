import vim

CURRENT_DIRECTORY = vim.eval("getcwd()")
KNOWLEDGE_DIRECTORY = f'{CURRENT_DIRECTORY}/.vim_domain_knowledge/'
DB_NAME = 'vim_domain_knowledge.db'
DICTIONARY_NAME = 'vim_domain_knowledge_dictionary.txt'
DB_PATH = f'{KNOWLEDGE_DIRECTORY}{DB_NAME}'
DICTIONARY_PATH = f'{KNOWLEDGE_DIRECTORY}{DICTIONARY_NAME}'
