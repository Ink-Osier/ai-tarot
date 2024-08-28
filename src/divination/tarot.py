from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

TAROT_PROMPT = "您将接受我的问题并进行塔罗牌阅读。 " \
    "我会给你提供我抽取出来的塔罗牌卡牌以及对应的正逆位 " \
    "请您根据我抽到的卡牌和问题仔细说明它们的意义，" \
    "解释哪张卡片属于未来或现在或过去，结合我的问题来解释它们，" \
    "并给我有用的建议或我现在应该做的事情."


class TarotFactory(DivinationFactory):
    divination_type = "tarot"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        user_prompt = divination_body.prompt.strip()
        if not user_prompt:
            raise HTTPException(status_code=400, detail="Prompt is empty")
        if len(user_prompt) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")

        # Assuming selected_cards is a list of dicts with 'name' and 'orientation'
        card_details = ", ".join([
            f"{card.name} ({card.orientation})" for card in divination_body.selected_cards
        ])
        type = divination_body.tarot_spread

        rule = f"本次占卜使用：{type}。"

        if(type == "塔罗牌-维纳斯牌阵（八张牌）"):
            rule = rule + "规则如下：八张牌的含义如下：1. 自己的真实想法：你对这段关系的内心真实感受。2. 对方的真实想法：对方对这段关系的内心真实感受。3. 彼此关系对自己的影响：这段关系对你产生的影响。4. 彼此关系对对方的影响：这段关系对对方产生的影响。5. 你们将会遇到的障碍：在这段关系中可能会遇到的挑战或困难。6. 最后的结果：这段关系可能会走向的最终结局。7. 将来自己的心情：未来你对这段关系的感受和情绪变化。8. 将来对方的心情：未来对方对这段关系的感受和情绪变化。"


        full_prompt = f"{TAROT_PROMPT}. {rule}.\n{user_prompt} The selected cards are: {card_details}."

        return full_prompt, ""