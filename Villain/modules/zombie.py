from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights

from Villain import DEMONS, DEV_USERS, DRAGONS, OWNER_ID, telethn

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS

# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern=f"^[!/]zombies ?(.*)"))
async def zombies(event):
    """ For .zombies command, list all the zombies in a chat. """

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "bahanchod Ek bhi Deleted Accounts nhi Found, Group Is Clean savach bharat abhiyan."

    if con != "clean":
        find_zombies = await event.respond("Searching For Zombies hmm starting savach group abhiyan.")
        async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"Found **{del_u}** Zombies In This Group.\
            \nClean Them By Using - `/zombies clean`"
        await find_zombies.edit(del_status)
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not await is_administrator(user_id=event.from_id, message=event):
        await event.respond("You're Not An Admin!")
        return

    if not admin and not creator:
        await event.respond("I Am Not An Admin Here first promote me with full rights!")
        return

    cleaning_zombies = await event.respond("Cleaning Zombies Group ko saaf kr dege...")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await cleaning_zombies.edit("I Don't Have Ban Rights In This Group first and last bar bolta hu give me all rights.")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned `{del_u}` Zombies"

    if del_a > 0:
        del_status = f"Cleaned `{del_u}` Zombies \
        \n`{del_a}` Zombie Admin Accounts Are Not Removed admin ki bahut respect krta hu"

    await cleaning_zombies.edit(del_status)
