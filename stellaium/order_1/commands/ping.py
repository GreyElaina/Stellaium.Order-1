from graia.saya import Saya, Channel
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.message import MessageEvent
from graia.ariadne import Ariadne


saya = Saya.current()
channel = Channel.current()

@channel.use(CommandSchema("/ping"))
async def ping_command(app: Ariadne, event: MessageEvent):
    await app.sendMessage(event, MessageChain.create(Plain("pong!")))