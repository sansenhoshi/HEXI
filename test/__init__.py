from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent
from hexi.plugins.core.message_handle import MessageState
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.typing import T_State

__plugin_meta__ = PluginMetadata(
    "测试",
    "测试",
    "测试",
)

test = on_command("测试", aliases={"测试"})


@test.handle()
async def handle_test(event: MessageEvent,state:T_State):
    m_state = MessageState(state)
    cmd = m_state.get_command()
    msg = m_state.get_command_arg()
    uid = event.user_id
    gid = event.group_id
    nickname = event.sender.nickname
    mes = f"测试所在群聊：{gid}\n" \
          f"测试发送者：{uid}\n" \
          f"测试者昵称：{nickname}\n" \
          f"测试附加内容：{msg}\n" \
          f"测试触发的命令：{cmd}"
    await test.finish(mes)
