from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from .bf2042 import bf_2042_gen_pic
from .data import query_data
from ..core.message_handle import MessageState

__plugin_meta__ = PluginMetadata(
    name="2042战绩查询",
    description="根据对应指令查询对应数据",
    usage="发送 [.盒/.数据/.武器/.配备/.专家/.载具] 游戏ID",
    type="application",
)

status_aliases = {".盒", ".数据", ".武器", ".配备", ".专家", ".载具"}

status = on_command("2042战绩", aliases=status_aliases)


@status.handle()
async def handle_status(event: MessageEvent, state: T_State):
    m_state = MessageState(state)
    cmd = m_state.get_command()
    msg = m_state.get_command_arg()
    a = {".盒": 0,
         ".武器": 1,
         ".配备": 3,
         ".专家": 4,
         ".载具": 5
         }
    if msg is None:
        await status.send("消息是空的喵")
    else:
        msg_info = (MessageSegment.text(f"消息是{msg.text}"))
        await status.send(msg_info)
    print(state)
    print(m_state)
    message_id = event.message_id

    # img_mes = await query_data(player, "pc", query_type)
    # if img_mes[0]:
    #     res = MessageSegment.image(img_mes[1])
    # else:
    #     res = MessageSegment.text(img_mes[1])
    # msg_gen = (MessageSegment.reply(message_id), res)
