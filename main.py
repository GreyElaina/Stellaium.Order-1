import asyncio
from graia.broadcast import Broadcast
from graia.ariadne import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import MiraiSession
from graia.ariadne.message.commander import Commander
from graia.ariadne.event.message import MessageEvent
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import BroadcastBehaviour
from graia.scheduler.saya.behaviour import GraiaSchedulerBehaviour
from graia.scheduler import GraiaScheduler
from graia.ariadne.message.commander.saya import CommanderBehaviour

loop = asyncio.new_event_loop()
broadcast = Broadcast(loop=loop)
app = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        host="http://localhost:8080",  # 填入 HTTP API 服务运行的地址
        verify_key="test",  # 填入 verifyKey
        account=1779309090,  # 你的机器人的 qq 号
    ),
    chat_log_config=False
)
commander = Commander(broadcast)
saya = Saya(broadcast)
scheduler = GraiaScheduler(loop, broadcast)

saya.install_behaviours(
    BroadcastBehaviour(broadcast),
    GraiaSchedulerBehaviour(scheduler),
    CommanderBehaviour(commander),
)

with saya.module_context():
    saya.require("stellaium.order_1")

app.launch_blocking()