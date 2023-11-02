from nonebot.adapters.onebot.v11 import MessageSegment


class TextMessage:
    def __init__(self, text):
        self.text = text


class ImageMessage:
    def __init__(self, image):
        self.image = image


class UnknownMessage:
    def __init__(self, raw):
        self.raw = raw


class MessageState:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    # 获取命令头
    def get_command(self):
        return self.data_dict['_prefix']['command']

    # 获取命令参数
    def get_command_arg(self):
        command_arg_list = self.data_dict['_prefix']['command_arg']
        if command_arg_list:
            command_arg = command_arg_list[0]
            if isinstance(command_arg, MessageSegment):
                if command_arg.type == 'text':
                    return TextMessage(command_arg.data['text'])
                elif command_arg.type == 'image':
                    return ImageMessage(command_arg.data['url'])
        return None  # 返回 None 表示命令参数为空或无法解析
