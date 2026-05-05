def process_payment(amount: float):
    if amount > 1000:
        return {"status": "failed"}
    return {"status": "success"}


if __name__ == "__main__":
    print("Payment service running (placeholder)")