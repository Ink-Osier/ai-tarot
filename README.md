# AI Tarot

> [!IMPORTANT]
>
> 本项目为在项目[chatgpt tarot divination](https://github.com/dreamhunter2333/chatgpt-tarot-divination)基础上二开而来。

## AI 占卜 功能列表

- [x] 塔罗牌（三张牌占卜法）
- [x] 塔罗牌（维纳斯牌阵）

![demo](a![image](https://github.com/user-attachments/assets/a4dd8d48-9e67-40ff-b1ad-8e5bea3035f6))

## Deploy by docker

```yaml
services:
  ai-tarot:
    image: wizerd/ai-tarot:latest
    container_name: ai-tarot
    restart: always
    ports:
      - 43222:8000
    environment:
      - api_key=<OPENAI 密钥>
      - api_base=<API BASE URL> # optional
      - model=gpt-4o # optional
      # - rate_limit=10/minute # optional
      # - user_rate_limit=600/hour # optional
      - github_client_id=xxx
      - github_client_secret=xxx
      - jwt_secret=secret
      - ad_client=ca-pub-xxx
      - ad_slot=123
```
