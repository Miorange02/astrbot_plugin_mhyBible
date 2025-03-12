import logging
import random
import requests  # 导入requests库
import json  # 导入 json 模块以处理 JSON 文件
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType

logger = logging.getLogger(__name__)

# 读取 JSON 文件中的列表
try:
    with open('ys_text_list.json', 'r', encoding='utf-8') as f:
        ys_text_list = json.load(f)
except FileNotFoundError:
    logger.error("ys_text_list.json 文件未找到，请检查文件路径。")
    ys_text_list = []
except json.JSONDecodeError:
    logger.error("ys_text_list.json 文件格式错误，请检查文件内容。")
    ys_text_list = []


@register("astrbot_plugin_mhyBible", "orange8938", "返回原神等网络圣经的插件", "1.0", "repo url")
class GenshinImpactPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.genshin_mention_count = 0  # 初始化连续提到“原神”的次数为 0
        self.is_plugin_active = True  # 插件激活状态

    def log_message_debug_info(self, msg_obj):
        logger.debug("=== Debug: AstrBotMessage ===")
        logger.debug("Bot ID: %s", msg_obj.self_id)
        logger.debug("Session ID: %s", msg_obj.session_id)
        logger.debug("Message ID: %s", msg_obj.message_id)
        logger.debug("Sender: %s", msg_obj.sender)
        logger.debug("Group ID: %s", msg_obj.group_id)
        logger.debug("Message Chain: %s", msg_obj.message)
        logger.debug("Raw Message: %s", msg_obj.raw_message)
        logger.debug("Timestamp: %s", msg_obj.timestamp)
        logger.debug("============================")

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        if not self.is_plugin_active:
            return  # 如果插件已关闭，直接返回

        msg_obj = event.message_obj
        text = msg_obj.message_str or ""
        self.log_message_debug_info(msg_obj)

        if "原神" or "OP" in text:
            self.genshin_mention_count += 1
            if self.genshin_mention_count >= 18:  # 连续提到 18 次触发彩蛋
                yield event.plain_result("学长收收味,我要拉黑你~怒(warn:插件已关闭)")
                self.is_plugin_active = False  # 关闭插件
            else:
                if ys_text_list:
                    selected_text = random.choice(ys_text_list)
                    yield event.plain_result(selected_text)
        else:
            self.genshin_mention_count = 0  # 重置计数
