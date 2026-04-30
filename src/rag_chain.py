import streamlit as st
import time
import json
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from prompts import QA_PROMPT, SUMMARY_PROMPT, ANOMALY_PROMPT, CHART_DATA_PROMPT
from vector_store import get_retriever

class APIKeyError(Exception):
    pass

class RateLimitError(Exception):
    pass

class LLMError(Exception):
    pass

def get_llm():
    if "GROQ_API_KEY" not in st.secrets or not st.secrets["GROQ_API_KEY"]:
        raise APIKeyError(
            "Groq API key not found. Please add it to `.streamlit/secrets.toml`:\n"
            "```\nGROQ_API_KEY = \"gsk_your_key_here\"\n```"
        )

    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=st.secrets["GROQ_API_KEY"],
        temperature=0.3,
        timeout=30,
        max_retries=2,
    )
    return llm

def _safe_invoke(chain, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.invoke(query)

        except Exception as e:
            error_msg = str(e).lower()

            if "rate_limit" in error_msg or "429" in error_msg or "too many requests" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    st.warning(f"⏳ Rate limit hit. Retrying in {wait_time}s... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RateLimitError(
                        "Rate limit exceeded. Groq free tier allows 30 requests/minute. "
                        "Please wait a minute and try again."
                    )

            elif "auth" in error_msg or "401" in error_msg or "invalid api key" in error_msg:
                raise APIKeyError(
                    "Invalid Groq API key. Please check your key in `.streamlit/secrets.toml`. "
                    "Get a free key at https://console.groq.com"
                )

            elif "timeout" in error_msg or "timed out" in error_msg:
                if attempt < max_retries - 1:
                    st.warning(f"⏳ Request timed out. Retrying... (attempt {attempt + 2}/{max_retries})")
                    continue
                else:
                    raise LLMError(
                        "Request timed out after multiple attempts. "
                        "The server may be overloaded. Please try again later."
                    )

            elif "connection" in error_msg or "network" in error_msg:
                raise LLMError(
                    "Network error. Please check your internet connection and try again."
                )

            else:
                raise LLMError(f"An unexpected error occurred: {str(e)}")

    raise LLMError("Failed after maximum retries.")

def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_qa_chain(vector_store):
    llm = get_llm()
    retriever = get_retriever(vector_store, k=4)

    chain = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough()
        }
        | QA_PROMPT
        | llm
        | StrOutputParser()
    )

    return {"chain": chain, "retriever": retriever}

def ask_question(qa_chain_dict, question):
    chain = qa_chain_dict["chain"]
    retriever = qa_chain_dict["retriever"]

    answer = _safe_invoke(chain, question)
    source_docs = retriever.invoke(question)

    return {"result": answer, "source_documents": source_docs}

def get_summary(vector_store, llm=None):
    if llm is None:
        llm = get_llm()
    retriever = get_retriever(vector_store, k=6)

    chain = (
        {"context": retriever | _format_docs}
        | SUMMARY_PROMPT
        | llm
        | StrOutputParser()
    )

    return _safe_invoke(chain, "Summarize this billing document")

def detect_anomalies(vector_store, llm=None):
    if llm is None:
        llm = get_llm()
    retriever = get_retriever(vector_store, k=6)

    chain = (
        {"context": retriever | _format_docs}
        | ANOMALY_PROMPT
        | llm
        | StrOutputParser()
    )

    return _safe_invoke(chain, "Detect anomalies in this billing document")

def get_chart_data(vector_store, llm=None):
    if llm is None:
        llm = get_llm()
    retriever = get_retriever(vector_store, k=6)

    chain = (
        {"context": retriever | _format_docs}
        | CHART_DATA_PROMPT
        | llm
        | StrOutputParser()
    )

    raw_response = _safe_invoke(chain, "Extract billing data for charts")

    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return data
    except (json.JSONDecodeError, IndexError):
        return None
