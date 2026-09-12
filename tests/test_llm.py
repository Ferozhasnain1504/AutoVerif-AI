from agent.llm_client import LLMClient


def main():

    llm = LLMClient()

    response = llm.generate(
        "Explain in one sentence what a 4-bit adder does."
    )

    print("\n========== GEMINI RESPONSE ==========")

    print(response)


if __name__ == "__main__":
    main()