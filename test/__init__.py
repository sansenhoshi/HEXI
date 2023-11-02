from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent

__plugin_meta__ = PluginMetadata(
    "测试",
    "测试",
    "测试",
)

test = on_command("测试", aliases={"测试"})


@test.handle()
async def handle_test(event: MessageEvent):
    msg = str(event.message).split(" ")[1]
    uid = event.user_id
    gid = event.group_id
    nickname = event.sender.nickname
    mes = f"测试所在群聊：{gid}\n" \
          f"测试发送者：{uid}\n" \
          f"测试者昵称：{nickname}\n" \
          f"测试附加内容：{msg}"
    await test.finish(mes)
