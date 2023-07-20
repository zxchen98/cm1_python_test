import random
import os
import discord
from discord.ext import commands

import streamlit as st
import openai
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

TOKEN = "MTEyOTQ1NjExMDIxOTMxNzMwOA.GDh4h9.Iza8AS3ozuR7V2n5wkXwbs-D12v079ZQDaFQsg"

# Create the template for langchain
template = """
You are a bot of my discord channel, you need to first greet the user and make a joke of his name and then answer any questions they might have.
{history}
Human: {user_input}
Chatbot:
"""
# create the prompt
prompt = PromptTemplate(
    input_variables=["history","user_input"],
    template=template,
)

# load chat model
# Set the temperature to be 0.7 to enable higher creativity
chat = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo",openai_api_key = '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')

# creating the memory
memory = ConversationBufferWindowMemory(memory_key="history",k=2)

# create a chain
joke_chain = LLMChain(llm=chat, prompt=prompt,memory=memory,verbose=True)

# create the discord client with intent
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = joke_chain.predict(user_input=str(message.author)+str(message.content))

    await message.channel.send(str(text))

client.run(TOKEN)