DATA_CONFIGS = {
    'encoding' : 'windows-1252'
}

DESCRIPTION_CONFIGS = {
    'encoding' : 'utf-8'
    , 'parser': 'html.parser'
    , 'breaking_spaces': {
        'pattern': '\xa0'
        , 'repl': ' '
    }
    , 'weird_characters': {
        'pattern': '�'
        , 'repl': ''
    }
    , 'section_name': {
        'pattern': r'Section\s+Name:\s*'
        , 'repl': 'Section Name: '
    }
    , 'sas_variable_name': {
        'pattern': r'SAS\s+Variable\s+Name:\s*'
        , 'repl': 'SAS Variable Name: '
    }
}