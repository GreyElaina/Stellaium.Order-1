from gql import gql
from graia.saya import Saya, Channel
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.commander import Slot, Arg
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.message import MessageEvent
from graia.ariadne import Ariadne
from loguru import logger
from gql.transport.exceptions import TransportQueryError
from stellaium.order_1.github import github_gql
import importlib.resources as pkg_resources
from asyncio.exceptions import TimeoutError
import re
from .. import resources

saya = Saya.current()
channel = Channel.current()


@channel.use(CommandSchema("/repo {repo}", {"repo": Slot("repo", str)}))
async def simple_repo_info(app: Ariadne, event: MessageEvent, repo: str):
    if not re.match(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$", repo):
        await app.sendMessage(
            event, MessageChain.create(Plain("请输入正确的仓库名称, 格式为, <owner>/<name>"))
        )
        return
    owner = repo.split("/")[0]
    name = repo.split("/")[1]
    await app.sendMessage(event, MessageChain.create(Plain(f"正在查询 {repo} 的信息...")))
    with pkg_resources.path(resources, "simple_repo_info.gql") as file:
        query = gql(file.read_text())
    try:
        result = await github_gql.execute_async(
            query,
            parse_result=True,
            serialize_variables=True,
            variable_values={"owner": owner, "name": name},
        )
    except Exception as e:
        logger.exception(e)
        if isinstance(e, TransportQueryError):
            assert isinstance(e.data, dict)
            assert isinstance(e.errors, list)
            if e.errors[0]['type'] == "NOT_FOUND":
                await app.sendMessage(
                    event, MessageChain.create(Plain("发生错误: 没有找到相关仓库"))
                )
                return
            else:
                await app.sendMessage(event, MessageChain.create(f"发生错误: {e.__class__.__name__}"))
        elif isinstance(e, TimeoutError):
            await app.sendMessage(event, MessageChain.create(Plain("查询超时, 请重试.")))
        return

    if not result['repository']:
        await app.sendMessage(event, MessageChain.create(Plain("发生错误: 没有找到相关仓库")))
        return
    await app.sendMessage(event, MessageChain.create("\n".join([
        f"仓库: {repo}",
        f"仓库描述: {result['repository']['description']}",
        f"仓库链接: {result['repository']['url']}",
        f"仓库创建时间: {result['repository']['createdAt']}",
        f"仓库更新时间: {result['repository']['updatedAt']}",
        f"上次推送: {result['repository']['pushedAt']}",
        f"上次 Commit: {result['repository']['defaultBranchRef']['target']['history']['nodes'][0]['committedDate']}",
        f"Star 数: {result['repository']['stargazers']['totalCount']}",
        f"Watcher 数: {result['repository']['watchers']['totalCount']}",
        f"Issue 开启数: {result['repository']['issues']['totalCount']}",
        f"Pull Request 开启数: {result['repository']['pullRequests']['totalCount']}",
        f"使用协议: {result['repository']['licenseInfo']['name']}",
    ])))
