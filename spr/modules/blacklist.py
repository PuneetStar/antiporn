from pyrogram import filters
from pyrogram.types import Message
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat
from spr import SUDOERS, spr
from spr.modules.info import get_info


@spr.on_message(
    filters.command("blacklist") & filters.user(SUDOERS), group=3
)
async def blacklist_func(_, message: Message):
    err = "Enter a user/chat's id"
    if len(message.command) != 2:
        return await message.reply_text(err)
    id = message.text.split(None, 1)[1]
    if not id:
        return await message.reply_text(err)
    try:
        id = int(id)
    except ValueError:
        return await message.reply_text(err)

    if id == 0:
        return await message.reply_text(err)

    if id < 0:
        try:
            chat = await spr.get_chat(id)
        except Exception as e:
            return await message.reply_text(str(e))
        if not await is_served_chat(id):               
               await add_served_chat(id)
        if id in await blacklisted_chats():
               return await message.reply_text(
                "This chat is already blacklisted."
            )
        await black_chat(id)
        await message.reply_text(f"Blacklisted chat {chat.title}")

    if id in SUDOERS:
        return await message.reply_text(
            "This user is in SUDOERS and cannot be blacklisted."
        )
    try:
        user = await spr.get_users(id)
    except Exception as e:
        return await message.reply_text(str(e))
        if not await is_served_user(id):                                
               await add_served_user(id)
        is_gbanned = await is_gbanned_user(id)
        if is_gbanned:
            return await message.reply_text(
            "This user is already blacklisted."
        )
    await add_gban_user(id)
    await message.reply_text(f"Blacklisted user {user.mention}")


@spr.on_message(
    filters.command("whitelist") & filters.user(SUDOERS), group=3
)
async def whitelist_func(_, message: Message):
    err = "Enter a user/chat's id."
    if len(message.command) != 2:
        return await message.reply_text(err)
    id = message.text.split(None, 1)[1]
    try:
        id = int(id)
    except ValueError:
        return await message.reply_text(err)
    if id == 0:
        return await message.reply_text(err)
    if id < 0:
        try:
            chat = await spr.get_chat(id)
        except Exception as e:
            return await message.reply_text(str(e))

        is_serve = await is_served_chat(id)
        if not is_serve:              
               await add_served_chat(id)
        if id not in await blacklisted_chats():                
               return await message.reply_text(
                "This chat is already whitelisted."
            )
        await white_chat(id)
        return await message.reply_text(f"Whitelisted {chat.title}")

    try:
        user = await spr.get_users(id)
    except Exception as e:
        return await message.reply_text(str(e))

        is_served = await is_served_user(id)
        if not is_served:           
           await add_served_user(id)
           is_gbanned = await is_gbanned_user(id)         
           if not is_gbanned:              
              return await message.reply_text(
            "This user is already whitelisted."
        )
    await remove_gban_user(id)
    return await message.reply_text(f"Whitelisted {user.mention}")
