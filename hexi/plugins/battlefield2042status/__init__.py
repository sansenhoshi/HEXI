from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from .picture_builder import builder
from .data import query_data, get_img
from ..core.message_handle import MessageState

__plugin_meta__ = PluginMetadata(
    name="2042战绩查询",
    description="根据对应指令查询对应数据",
    usage="发送 [.盒/.数据/.武器/.配备/.专家/.载具] 游戏ID",
    type="application",
)

status_aliases = {"/数据", "/武器", "/配备", "/专家", "/载具"}

status = on_command("2042战绩", aliases=status_aliases)


@status.handle()
async def handle_status(event: MessageEvent, state: T_State):
    m_state = MessageState(state)
    print(state)
    cmd = m_state.get_command()
    msg = m_state.get_command_arg()
    cmd = cmd[0]
    property = {"/数据": "0",
                "/武器": "weapons",
                "/配备": "gadgets",
                "/专家": "classes",
                "/载具": "vehicles"
                }
    msg_info = (MessageSegment.text(f"正在查询 {msg.text} 的 {cmd.replace('/', '')} 数据，请耐心等待"))
    await status.send(msg_info)
    img_mes = await query_data(msg.text, 'pc', cmd)
    message_id = event.message_id
    if img_mes[0]:
        res = MessageSegment.image(img_mes[1])
    else:
        res = MessageSegment.text(img_mes[1])
    msg_gen = (MessageSegment.reply(message_id), res)
    await status.finish(msg_gen)
