
from pyrogram import types
from aiohttp import ClientSession
from typing import Dict, Optional
from dataclasses import dataclass

import logging
import json




expireDataLink = "https://dpaste.org/MaFJd"
expires_data =  (
        ("onetime", "One-Time snippet"),
        (3600, "Expire in one hour"),
        (3600 * 24 * 7, "Expire in one week"),
        (3600 * 24 * 30, "Expire in one month"),
        ("never", "Never Expire"),
  )


highlightsDataLink = "https://dpaste.org/VydUY"
highlights_data = (
("_text", "Plain text"), ("_code", "Plain code"),
("applescript", "AppleScript"),
("arduino", "Arduino"),("bash", "Bash"),("bat", "Batchfile"),
("c", "C"),("coffee-script", "CoffeeScript"), ("common-lisp", "Common Lisp"),
("cmake", "CMake"), ("clojure", "Clojure"),("console", "Console/Bash Session"),
("css", "CSS"),("csharp", "C#"),("cuda", "CUDA"),
("d", "D"), ("dart", "Dart"), ("delphi", "Delphi"), ("diff", "Diff"), ("django", "Django/Jinja"),
("docker", "Docker"),  ("handlebars", "Handlebars"),
("haskell", "Haskell"), ("go", "Go"), ("erlang", "Erlang"),
("elixir", "Elixir"), ("js", "JavaScript"), ("java", "Java"),
("objective-c", "Objective-C"), ("numpy", "NumPy"), ("nginx", "Nginx configuration file"), ("matlab", "Matlab"),
("lua", "Lua"), ("make", "Makefile"), ("php", "PHP"), ("perl", "Perl"),
("postgresql", "PostgreSQL SQL dialect"), ("python", "Python"),
("rb", "Ruby"), ("rst", "reStructuredText"), ("rust", "Rust"), 
("sql", "SQL"), ("swift", "Swift"), ("typoscript", "TypoScript"),
("xml", "XML"), ("yaml", "YAML"), ("xslt", "XSLT"), 
)





@dataclass
class paste:
    content: str
    lexer: str = "_text"
    expire: str = "604800"  # pasted will be deleted in a week
    format: str = "json"
    api_url: str = "https://dpaste.org/api/"
    
    
    @staticmethod
    def getLink(data: dict):
        url = data['url']
        paste_url = url
        raw_url = url + "/raw"
        return {
              'paste_url': paste_url,
              'raw_url': raw_url
           }
           
           
    @staticmethod
    def getExpiresButtons(lexer: str) -> types.InlineKeyboardButton:
         button_data = []
         row_data = []
         for i, expire in enumerate(expires_data, start=1):
                 button = types.InlineKeyboardButton(expire[1], callback_data="paste"+":"+lexer+":"+str(expire[0]))
                 row_data.append(button)
                 if i % 2 == 0:
                        button_data.append(row_data)
                        row_data = []
         if row_data:
         	      button_data.append(row_data)
         return button_data 
    

    @staticmethod
    def getHighLightsButtons() -> types.InlineKeyboardButton:
         button_data = []
         row_data = []
         for i, lang in enumerate(highlights_data, start=1):
                 button = types.InlineKeyboardButton(lang[1], callback_data="highlight:"+lang[0])
                 row_data.append(button)
                 if i % 4 == 0:
                        button_data.append(row_data)
                        row_data = []
         if row_data:
         	      button_data.append(row_data)
         return button_data 
        
         
     
    async def paste(self: dict) -> Optional[Dict]:
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36 OPR/84.0.0.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            'content': self.content,
            'lexer': self.lexer,
            'expire': self.expire,
            'format': self.format
        }
        
        async with ClientSession() as session:
            try:
                async with session.post(url=self.api_url, headers=headers, data=payload) as response:
                    if not response.ok:
                           return {'error': repr(response.reason)}
                    else:
                        try:
                             data = json.loads(await response.text())
                             return data
                        except Exception as e:
                             return {'error': repr(e)}
                             
            except Exception as e:
                  logger.error("An error occurred: %s", e)
                  return {'error': repr(e)}
  
  
                              