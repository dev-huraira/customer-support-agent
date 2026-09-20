from langchain_google_genai import ChatGoogleGenerativeAI
from tools.billing_tools import update_payment_method,check_invoices,process_refund
from langchain.agents import create_agent

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

billing_agent=create_agent(
    llm,
    tools=[check_invoices,process_refund,update_payment_method],
    system_prompt=("""You are a billing support agent. Help users with invoices,
refunds, and payment methods using the tools available to you."""),

 )
