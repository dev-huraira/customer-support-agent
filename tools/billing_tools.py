from langchain_core.tools import tool

MOCK_INVOICES = {
    "user_101": [
        {"invoice_id": "INV-001", "amount": 49.99, "status": "paid", "date": "2026-08-01"},
        {"invoice_id": "INV-002", "amount": 49.99, "status": "unpaid", "date": "2026-09-01"},
    ]
}

MOCK_PAYMENT_METHODS = {
    "user_101": {"type": "card", "last_four": "4242"}
}

@tool
def check_invoices(user_id:str) -> str:
    """Look up all invoices for a given user id and return there status"""
    invoices=MOCK_INVOICES.get(user_id)

    if not invoices:
        return f"No invoices found for user {user_id}"

    lines=[f"{inv['invoice_id']}: ${inv['amount']} - {inv['status']} (dated {inv['date']})"  for inv in invoices]
    return "\n".join(lines)


@tool
def process_refund(user_id:str,invoice_id:str) ->str:
    """Process the refund of specific invoice belonging to user id"""
    invoices = MOCK_INVOICES.get(user_id)
    if not invoices:
        return f"No invoices found for user {user_id}."

    for inv in invoices:
        if inv["invoice_id"] == invoice_id:
            if inv["status"] == "refunded":
                return f"{invoice_id} is allready refunded"
            inv["status"] = "refunded"
            return f"Refund processed for {invoice_id} (${inv['amount']})."
    return f"Invoice {invoice_id} not found for user {user_id}."


@tool
def update_payment_method(user_id:str,card_last_four:str) ->str:
    """Update the payment method on file for a user, given the new card's last four digits."""
    if not card_last_four.isdigit() or len(card_last_four) != 4:
        return "Invalid card number format. Please provide exactly 4 digits."

    MOCK_PAYMENT_METHODS[user_id] = {"type": "card", "last_four": card_last_four}
    return f"Payment method updated for {user_id}. Card ending in {card_last_four}."



 

    