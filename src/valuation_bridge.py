"""
GS Valuation Bridge
Weighted average: DCF 35%, Comps 30%, MC 20%, LBO 10%, M&A 5%
"""

WEIGHTS = {"DCF": 0.35, "Comps": 0.30, "Monte Carlo": 0.20,
           "LBO": 0.10, "M&A": 0.05}


def compute_bridge(model_prices: dict, current_price: float) -> dict:
    weighted = sum(model_prices[m] * WEIGHTS[m] for m in WEIGHTS)
    upside   = (weighted - current_price) / current_price * 100
    return {
        "target":   round(weighted, 2),
        "upside":   round(upside, 1),
        "rating":   "BUY" if upside > 15 else "HOLD" if upside > -5 else "SELL",
        "conviction": "High" if abs(upside) > 25 else "Medium" if abs(upside) > 10 else "Low",
    }