## TEST: EXAMPLE CODE ####

import asyncio
from utils import paste

TEXT = """\n
This an example of text for testing...
"""

async def main():
    paster = paste(TEXT, lexer='python')
    paste.lexer = "_text"
    print(await paster.paste())
    
asyncio.run(main())


## output

## {'url': 'https://dpaste.org/gg0av', 'content': '\n\nThis an example of text for testing...\n', 'lexer': '_text'}

