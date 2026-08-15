from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import time
import httpx
# Setup LLM
llm = ChatOpenAI(
    base_url = "https://163.17.136.119:8591/v1",
    api_key = "sk-9o0cj_Q6aJWWbSLODEPKBQ",
    model = "gemma-4-E4B-it",
    temperature = 0,
    max_tokens = 200,
    http_client = httpx.Client(verify=False),
)
# Setup Chain (different prompt templates for different social media platforms)
# Branch A: LinkedIn
linkedin_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是 LinkedIn 上的專業職涯顧問。請寫一段嚴肅、專業且具備商業洞察力的短評(50字內)。"),
        ("human", "主題：{topic}")
    ])
    | llm
    | StrOutputParser()
)

# Branch B: Instagram
ig_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是 Instagram 上的幽默網紅。請寫一段活潑、好笑的貼文，一定要包含表情符號(Emoji)和熱門 Hashtag (50字內)。"),
        ("human", "主題：{topic}")
    ])
    | llm
    | StrOutputParser()
)
# Parallel (combine both chains)
combo_chain = RunnableParallel(
    linkedin = linkedin_chain,
    instagram = ig_chain
)
# User input
target_topic = input("輸入主題： ")

# method A: streaming
# 觀察重點：不同欄位的文字會交錯出現
print(f"--- Method 1: Streaming 即時生成中... ---")
for chunk in combo_chain.stream({"topic": target_topic}):
    print(chunk)

# method B: batch
# 觀察重點：等待一段時間後，一次顯示完整結果
print(f"--- Method 2: Batch 批次生成中... ---")
start_time = time.time()
results = combo_chain.batch([{"topic": target_topic}])
end_time = time.time()
final_result = results[0]
print(f"耗時: {end_time - start_time:.2f} 秒")
print("-" * 50)
print(f"【LinkedIn】：\n{final_result['linkedin']}")
print("-" * 50)
print(f"【IG】：\n{final_result['instagram']}")
print("-" * 50)
