def apply_rules(data: dict):
    """
    Returns:
    - None → no rule triggered
    - dict → forced fraud decision
    """

    amount = data.get("amount", 0)
    oldbalance = data.get("oldbalanceOrg", 0)
    newbalance = data.get("newbalanceOrig", 0)
    tx_type = data.get("type", "")

    # 🚨 Rule 1: Empty account + transaction
    if oldbalance == 0 and amount > 50000:
        return {
            "fraud_prediction": 1,
            "fraud_probability": 0.95,
            "reason": "Empty account with large transaction"
        }

    # 🚨 Rule 2: Full drain
    if amount == oldbalance and newbalance == 0 and amount > 100000:
        return {
            "fraud_prediction": 1,
            "fraud_probability": 0.98,
            "reason": "Full account drain"
        }

    # 🚨 Rule 3: Very large transfer
    if tx_type == "TRANSFER" and amount > 300000:
        return {
            "fraud_prediction": 1,
            "fraud_probability": 0.92,
            "reason": "High-value transfer"
        }

    return None