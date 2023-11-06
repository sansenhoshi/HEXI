import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOTV11Adapter     # onebot v11
from nonebot.adapters.onebot.v12 import Adapter as OneBotV12Adapter     # onebot v12
from nonebot.adapters.minecraft import Adapter as minecraftAdapter      # minecraft
from nonebot.log import logger
from sqlalchemy import StaticPool

# 初始化 NoneBot 以及 数据库
nonebot.init(datastore_engine_options={"poolclass": StaticPool})

# 注册适配器
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOTV11Adapter)
driver.register_adapter(OneBotV12Adapter)
driver.register_adapter(minecraftAdapter)

# 加载自定义插件
nonebot.load_plugins("hexi")  # 加载bot自定义插件

# 加载配置文件中的插件
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    logger.warning("hexi？启动！")
    nonebot.run(app="__mp_main__:app")
