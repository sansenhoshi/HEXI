class PlayerStats:
    def __init__(self, data):
        self.userId = data["userId"]  # 用户ID
        self.avatar = data["avatar"]  # 用户头像URL
        self.userName = data["userName"]  # 用户名
        self.id = data["id"]  # ID
        self.bestClass = data["bestClass"]  # 最佳职业
        self.humanPrecentage = data["humanPrecentage"]  # 人类百分比
        self.kills = data["kills"]  # 击杀数
        self.deaths = data["deaths"]  # 死亡数
        self.wins = data["wins"]  # 胜利数
        self.loses = data["loses"]  # 失败数
        self.killsPerMinute = data["killsPerMinute"]  # 每分钟击杀数
        self.damagePerMinute = data["damagePerMinute"]  # 每分钟伤害
        self.killsPerMatch = data["killsPerMatch"]  # 每场比赛平均击杀数
        self.damagePerMatch = data["damagePerMatch"]  # 每场比赛平均伤害
        self.headShots = data["headShots"]  # 爆头击杀数
        self.winPercent = data["winPercent"]  # 胜率
        self.headshots = data["headshots"]  # 爆头比例
        self.killDeath = data["killDeath"]  # 击杀/死亡比率
        self.infantryKillDeath = data["infantryKillDeath"]  # 步兵击杀/死亡比率
        self.damage = data["damage"]  # 造成的总伤害
        self.timePlayed = data["timePlayed"]  # 游戏时间
        self.accuracy = data["accuracy"]  # 命中率
        self.revives = data["revives"]  # 复活队友次数
        self.heals = data["heals"]  # 治疗队友次数
        self.resupplies = data["resupplies"]  # 补给队友次数
        self.repairs = data["repairs"]  # 修复工具使用次数
        self.squadmateRevive = data["squadmateRevive"]  # 复活队友次数
        self.squadmateRespawn = data["squadmateRespawn"]  # 尝试复活但失败的次数
        self.thrownThrowables = data["thrownThrowables"]  # 扔出的可投掷物数量
        self.gadgetsDestoyed = data["gadgetsDestoyed"]  # 摧毁敌方设备数量
        self.callIns = data["callIns"]  # 呼叫支援次数
        self.playerTakeDowns = data["playerTakeDowns"]  # 击倒敌方玩家数
        self.matchesPlayed = data["matchesPlayed"]  # 游戏场次
        self.secondsPlayed = data["secondsPlayed"]  # 游戏时间（秒）
        self.bestSquad = data["bestSquad"]  # 最佳小队排名
        self.teammatesSupported = data["teammatesSupported"]  # 支持的队友数
        self.saviorKills = data["saviorKills"]  # 挽救友军次数
        self.shotsFired = data["shotsFired"]  # 开火次数
        self.shotsHit = data["shotsHit"]  # 命中次数
        self.killAssists = data["killAssists"]  # 协助击杀数
        self.vehiclesDestroyed = data["vehiclesDestroyed"]  # 摧毁的敌方载具数
        self.enemiesSpotted = data["enemiesSpotted"]  # 发现敌人次数
        self.mvp = data["mvp"]  # MVP 次数
        self.weapons = sorted(data["weapons"], key=lambda k: k['kills'], reverse=True)  # 武器列表 按击杀倒序排列
        self.vehicles = sorted(data["vehicles"], key=lambda k: k['kills'], reverse=True)    # 载具列表 按击杀倒序排列
        self.weaponGroups = data["weaponGroups"]    # 武器组
        self.vehicleGroups = data["vehicleGroups"]  # 载具组
        self.classes = sorted(data["classes"], key=lambda k: k['kills'], reverse=True)  # 专家列表 按击杀倒序排列
        self.gamemodes = sorted(data["gamemodes"], key=lambda k: k['secondsPlayed'], reverse=True)  # 游戏模式列表 按时长倒序排列
        self.maps = sorted(data["maps"], key=lambda k: k['secondsPlayed'], reverse=True)    # 地图列表 按时长倒序排列
        self.gadgets = sorted(data["gadgets"], key=lambda k: k['secondsPlayed'], reverse=True)  # 小工具/配备 列表
        self.dividedKills = data['dividedKills']
