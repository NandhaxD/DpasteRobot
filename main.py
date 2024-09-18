

import logging

from utils import paste
from pyrogram import Client, filters, types




logging.basicConfig(level=logging.INFO)


nandhaBot = Client(
name="d-paste",
api_id=123456,
api_hash="abcd",
bot_token="abcd"
)



def _filter_document(filter, client, update):
	       if update.document:
	       	     document = update.document
	       	     mime = document.mime_type
	       	     file_size = document.file_size
	       	     return (mime.startswith("text") or mime.startswith("application")) and (file_size/(1024 * 1024)) < 1 


filter_document = filters.create(_filter_document)




@nandhaBot.on_message(filters.command(['start', 'help']))
async def _start(client, message):
	         text = (f"**Hello there, {message.from_user.full_name}, I'm a paster bot that who can paste your code, text, document to https://dpaste.org.\n\nMy Channel @NandhaBots**")
	         msg = await message.reply_text(text, quote=True)
	         await msg.stop_propagation()
	         
	
	
	
	
async def get_content(m: types.CallbackQuery):
		     if m.text:
		     	    return m.text
		     else:
		     	    await m.edit_caption("**⚡ Reading document please wait...**")
		     	    file = await m.download()
		     	    with open(file, "r") as file:
		     	    	       content = file.read()
		     	    	       return content
	
	
	
@nandhaBot.on_callback_query()
async def _callback_query(bot: nandhaBot, query: types.CallbackQuery):
		        q_data = query.data
		        
		        if q_data.startswith('highlight'):
		        	        lexer = q_data.split(':')[1]
		        	        button_data = paste.getExpiresButtons(lexer)
		        	        buttons = types.InlineKeyboardMarkup(button_data)
		        	        return await query.message.edit_reply_markup(buttons)
		        	        
		        elif q_data.startswith("paste"):
	         	         _, lexer, expire = q_data.split(":")
	         	         content = await get_content(query.message)
	         	         paster = await paste(content, lexer=lexer, expire=expire).paste()
	         	         if 'error' in paster:
	         	         	    return await query.message.reply_text("❌ Error: %s" % paster['error'])
	         	         else:
	         	         	      paste_data = paste.getLink(paster)
	         	         	      
	         	         	      buttons = types.InlineKeyboardMarkup([[
	         	         	      types.InlineKeyboardButton("✨ Raw", url=paste_data["raw_url"]),
	         	         	      types.InlineKeyboardButton("✨ Paste", url=paste_data["paste_url"])
	         	         	      ]])
	         	         	      await query.message.edit_text(
                                  text=("**Thank you for using me. Join My @NandhaBots Channel**.\n\n**Paste Link**: %s\n**Raw Link**: %s" % (paste_data["paste_url"], paste_data["raw_url"])),
                                  reply_markup=buttons)
	         	         	   
	         	         
	         	        
	
FILTERS =  (filters.text | filter_document)
@nandhaBot.on_message(FILTERS, group=2)
async def _paste(bot, message):
	          
	          m = message
	          text = message.text
	          
	          button_data = paste.getHighLightsButtons()
	          buttons = types.InlineKeyboardMarkup(button_data)
	          
	          if text:
	          	     await message.reply_text(text, reply_to_message_id=m.id, reply_markup=buttons)
	          else:
	                await message.copy(chat_id=m.chat.id, reply_markup=buttons, reply_to_message_id=m.id)
	           
	          
	


nandhaBot.run()
