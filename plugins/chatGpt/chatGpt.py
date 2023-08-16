import logging
import openai
import os
import tiktoken
from errbot import BotPlugin

log = logging.getLogger("kchat.chatgpt")
log.setLevel(logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.util.logging.getLogger().setLevel(logging.WARNING)

model = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(model)


class ChatGpt(BotPlugin):
    """
    Chat GPT
    """
    max_model_tokens = 4000

    def activate(self):
        super().activate()
        self.start_poller(60, self.set_online)
        if 'CONVERSATIONS' not in self:
            self['CONVERSATIONS'] = {}
        return self

    def set_online(self):
        self._bot.change_presence()

    def callback_mention(self, message, mentioned_people):
        if self.bot_identifier not in mentioned_people:
            return

        log.info(f"message from {message.frm.person}")

        if hasattr(message.frm, "channelid"):
            conversation_id = message.frm.channelid
            self._bot.user_is_typing(conversation_id, message.parent.get("id") if message.is_threaded else None)
        else:
            conversation_id = message.frm.person

        prompt = message.body.replace(f"@{self.bot_identifier.username}", "").strip()

        if prompt.lower() in ["reset!", "reset"]:
            with self.mutable('CONVERSATIONS') as d:
                if conversation_id in self['CONVERSATIONS']:
                    del d[conversation_id]
            self.send(message.to, "Conversation was reset!")

            return

        messages = self['CONVERSATIONS'][conversation_id] if conversation_id in self['CONVERSATIONS'] else [{"role": "system", "content": "You are a helpful assistant."},]

        messages.append({"role": "user", "content": prompt})

        if len(encoding.encode(''.join([row['content'] for row in messages]))) > self.max_model_tokens:
            self.send(
                message.to,
                "You reached the maximum length for our conversation :sad-cat:\n Please reset it by saying: Reset!"
            )

        try:
            response = openai.ChatCompletion.create(model=model, messages=messages)
        except openai.error.RateLimitError:
            self.send(message.to, "I am to busy right now I can't answer!")

            return
        except:
            self.send(message.to, "Sorry I have an issue!")

            return

        response = response['choices'][0]['message']['content']

        self.send(message.to, response, in_reply_to=message if message.is_threaded else None)

        messages.append({"role": "assistant", "content": response})

        with self.mutable('CONVERSATIONS') as conversations:
            conversations[conversation_id] = messages
