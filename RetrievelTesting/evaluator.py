import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API"]

# Initialize the LLM (ensure your API key is set in your environment)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    max_tokens=None,
    timeout=None
)

fair_use_relation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a legal expert. Given the summary of a legal opinion regarding Fair Use and the description of an undecided case dispute, explain how the legal opinion relates to the dispute and what implications it might have on the case.\n\n  Evaluate the following legal opinion with respect to the four Fair Use factors. State whether the legal opinion provides support for Fair Use, is against Fair Use, or is not relevant for the Fair Use analysis."
        ),
        ("human", "Summary: {summary}\n\nDispute: {dispute}"),
    ]
)

fair_use_relation_chain = fair_use_relation_prompt | llm


@st.cache_data
def evaluate_case(summary, dispute):
    evaluation = fair_use_relation_chain.invoke({
        "summary": summary,
        "dispute": dispute
    })

    return evaluation.content
