import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import polars as pl
from util import evaluation_template
import time

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

rewrite_in_context_of_fair_use = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Rewrite the following copyright dispute in the context of the fair use four-factor test. For each of the four factors, provide a brief analysis relevant to the facts of the dispute, using neutral language suitable for legal or academic discussion. The four factors are: (1) the purpose and character of the use; (2) the nature of the copyrighted work; (3) the amount and substantiality of the portion used; and (4) the effect of the use upon the potential market for or value of the copyrighted work. Clearly distinguish which parts of the dispute relate to each factor."""

        ),
        ("human", "Dispute: {dispute}"),
    ]
)

rewrite_in_context_of_fair_use_chain = rewrite_in_context_of_fair_use | llm

combine_evaluations_use = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Given the analyses from each relevant case, please combine all the evaluations and analyze whether the use in the following case qualifies as fair use under U.S. copyright law (17 U.S.C. § 107). Use the four-factor framework, and for each factor, present arguments in favor of fair use and against fair use, citing relevant case law on both sides where applicable. Conclude with a balanced summary weighing the four factors. Use the following structure:
            
            {evaluation_template}"""

        ),
        ("human", "CombinedEvals: {combined_evaluations}"),
    ]
)

combine_evaluations_use_chain = combine_evaluations_use | llm

@st.cache_data
def evaluate_case(summary, dispute):
    evaluation = fair_use_relation_chain.invoke({
        "summary": summary,
        "dispute": dispute
    })

    return evaluation.content

@st.cache_data
def rewrite_four_factor_test(dispute):
    rewrite = rewrite_in_context_of_fair_use_chain.invoke({
        "dispute": dispute
    })

    return rewrite.content

@st.cache_data
def analyze_all_cases(cases, dispute):

    evaluations = []

    for row in cases.iter_rows(named = True):

        case_evaluation = row["Case"] + "\n\n" + row["CourtName"] + "\n\n" + evaluate_case(row["Summary"], dispute)

        time.sleep(5)

        evaluations.append(case_evaluation)

    combined_evaluations = "\n\n".join(evaluations)

    analysis = combine_evaluations_use_chain.invoke({
        "evaluation_template": evaluation_template,
        "combined_evaluations": combined_evaluations
    })

    return analysis.content

    
