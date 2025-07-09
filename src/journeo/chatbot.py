import chainlit as cl
from journeo.main import run_agent


@cl.on_chat_start
async def start():
    await cl.Message(content="Hello, how can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    response = await run_agent(message.content)
    await cl.Message(content=response or "Sorry, I couldn't process your request.").send()