from graia.saya import Saya, Channel

saya = Saya.current()
channel = Channel.current()

with saya.module_context():
    saya.require("stellaium.order_1.commands.ping")
    saya.require("stellaium.order_1.github.commands.repo")