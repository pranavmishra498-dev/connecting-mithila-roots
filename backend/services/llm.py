from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# 1. Load environment variables
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.2
)


# 3. Create prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant for Connecting Mithila Roots. "
        "You help users understand Mithila, its culture, traditions, "
        "history, festivals and Maithili language. "
        "Give simple, clear and accurate answers."
    ),
    (
        "human",
        "{question}"
    )
])


# 4. Connect prompt with Gemini
chain = prompt | llm


# 5. Generate answer
def generate_answer(question: str):

    response = chain.invoke({
        "question": question
    })

    content = response.content

    if isinstance(content, list):

        answer = "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )

        return answer

    return content


# 6. Test Gemini
if __name__ == "__main__":

    answer = generate_answer(
        "What is Mithila famous for?"
    )

    print("\nGemini Answer:\n")
    print(answer)