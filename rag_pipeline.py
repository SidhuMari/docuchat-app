from groq import Groq

def ask_hr_bot(user_question, collection, api_key):

    client = Groq(api_key=api_key)

    # Step 1: Retrieve
    results = collection.query(
        query_texts=[user_question],
        n_results=1
    )

    retrieved_content = results["documents"][0][0]

    # Step 2: Generate
    system_prompt = f"""
    You are HR Assistant. Answer only based on context.
    If not found, say "I dont know based on the handbook".

    Context:
    {retrieved_content}
    """

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0
    )

    return completion.choices[0].message.content