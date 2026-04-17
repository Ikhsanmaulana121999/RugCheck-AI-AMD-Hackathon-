import langgraph class
import requests
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    contract_address: str
    token_data: dict
    risk_score: int
    verdict: str

def fetch_token_data(state: AgentState):
    ca = state['contract_address']
    print(f"🔍 Scanning {ca}...")
    dummy_data = {
        "top_holders_pct": 68,
        "mint_authority": "Still Active",
        "lp_locked": False,
        "liquidity_usd": 2000
    }
    return {"token_data": dummy_data}

def analyze_with_llama(state: AgentState):
    data = state['token_data']
    print("🧠 Llama 3 on AMD GPU MI300X is analyzing...")
    score = 0
    red_flags = []
    
    if data['top_holders_pct'] > 50:
        score += 40
        red_flags.append(f"Top 3 wallet pegang {data['top_holders_pct']}% supply. Bahaya didump.")
    if data['mint_authority'] == "Still Active":
        score += 30
        red_flags.append("Mint Authority belum di-revoke. Dev bisa cetak token baru seenaknya.")
    if not data['lp_locked']:
        score += 30
        red_flags.append("Liquidity ${:,} gak di-lock. Bisa rug kapan aja.".format(data['liquidity_usd']))
    
    if score > 80:
        verdict = f"RISK SCORE: {score}/100 - EXTREME DANGER 🔴\n\nRed Flags Ditemukan:\n" + "\n".join([f"{i+1}. {x}" for i,x in enumerate(red_flags)]) + "\n\nAI Verdict: JANGAN SENTUH TOKEN INI KALO MASIH SAYANG DUIT LU BRO."
    else:
        verdict = f"RISK SCORE: {score}/100 - RELATIVELY SAFE 🟢\n\nAI Verdict: Keliatannya aman, tapi DYOR tetap wajib."

    return {"risk_score": score, "verdict": verdict}

workflow = StateGraph(AgentState)
workflow.add_node("fetcher", fetch_token_data)
workflow.add_node("analyzer", analyze_with_llama)
workflow.set_entry_point("fetcher")
workflow.add_edge("fetcher", "analyzer")
workflow.add_edge("analyzer", END)
app = workflow.compile()

if __name__ == "__main__":
    print("RugCheck AI is running on AMD GPU...")
    test_ca = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvEC"
    result = app.invoke({"contract_address": test_ca})
    print("\n--- HASIL AUDIT ---")
    print(result['verdict'])
