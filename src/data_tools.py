"""
Data collection tools -- yFinance, VADER, Serper web search.
"""
import yfinance as yf
import pandas as pd
import numpy as np
import json
import requests
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def fetch_financials(ticker: str) -> str:
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="1y")
    ytd = ((hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1) * 100
    return json.dumps({
        "ticker": ticker,
        "price": round(float(hist["Close"].iloc[-1]), 2),
        "ytd_return": str(round(float(ytd), 1)) + "%",
        "market_cap_B": round((info.get("marketCap") or 0) / 1e9, 1),
        "trailing_pe": round(info.get("trailingPE") or 0, 1),
        "forward_pe": round(info.get("forwardPE") or 0, 1),
        "revenue_growth": str(round((info.get("revenueGrowth") or 0)*100, 1)) + "%",
        "fcf_B": round((info.get("freeCashflow") or 0) / 1e9, 1),
        "beta": round(info.get("beta") or 0, 2),
        "recommendation": info.get("recommendationKey", "N/A"),
    }, default=str)


def fetch_sentiment(ticker: str) -> str:
    news = yf.Ticker(ticker).news or []
    sia = SentimentIntensityAnalyzer()
    scores = [sia.polarity_scores(n.get("title", ""))["compound"]
              for n in news[:20] if n.get("title")]
    if not scores:
        return json.dumps({"error": "no news"})
    avg = float(np.mean(scores))
    return json.dumps({
        "count": len(scores),
        "avg_score": round(avg, 3),
        "label": "Bullish" if avg > 0.05 else "Bearish" if avg < -0.05 else "Neutral",
    })


def web_search(query: str) -> str:
    r = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.environ["SERPER_API_KEY"],
                 "Content-Type": "application/json"},
        json={"q": query, "num": 4},
        timeout=10,
    )
    items = r.json().get("organic", [])[:4]
    return "\n".join([
        "- " + i.get("title", "") + ": " + i.get("snippet", "")[:100]
        for i in items
    ])