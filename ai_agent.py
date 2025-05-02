import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

# 1. Default UI values
DEFAULTS = {
    "mol_active_tab": "overview",
    "grph_active_tab": "distribution",
    "corr_val": 0.0,
    "k1_val": 1.0,
    "k2_val": 1.0,
    "topX_val": 5,
    "simul_val": 100
}

# 2. Our single “tool” that merges any provided overrides
def set_ui_values(mol_active_tab=None, grph_active_tab=None,
                  corr_val=None, k1_val=None, k2_val=None,
                  topX_val=None, simul_val=None):
    params = DEFAULTS.copy()
    overrides = {
        "mol_active_tab": mol_active_tab,
        "grph_active_tab": grph_active_tab,
        "corr_val": corr_val,
        "k1_val": k1_val,
        "k2_val": k2_val,
        "topX_val": topX_val,
        "simul_val": simul_val
    }
    for k, v in overrides.items():
        if v is not None:
            params[k] = v
    return params

# 3. Function schema for the OpenAI API
functions = [
    {
        "name": "set_ui_values",
        "description": "Set UI slider and tab values for the graph renderer",
        "parameters": {
            "type": "object",
            "properties": {
                "mol_active_tab":       {"type": "string", "description": "Which molecule tab is active"},
                "grph_active_tab":      {"type": "string", "description": "Which graph tab is active"},
                "corr_val":             {"type": "number", "description": "Correlation value"},
                "k1_val":               {"type": "number", "description": "k1 slider value"},
                "k2_val":               {"type": "number", "description": "k2 slider value"},
                "topX_val":             {"type": "integer","description": "Top X percent"},
                "simul_val":            {"type": "integer","description": "Number of simulations"},
            },
            "required": []
        }
    }
]

# 4. System prompt
system_message = {
    "role": "system",
    "content": (
        "You are Copilot, a data-science helper embedded in a Dash app.\n"
        "- Prefer concise answers.\n"
        "- When the user asks for a graph or simulation, call the "
        "'set_ui_values' function.\n"
        "- If the user doesn't mention a parameter, leave it at its default."
    )
}

def chat_with_agent(user_input):
    messages = [
        system_message,
        {"role": "user", "content": user_input}
    ]

    # 1st pass: ask GPT, allow it to call our function
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    msg = resp.choices[0].message

    if msg.get("function_call"):
        # Extract arguments and call our tool
        args = json.loads(msg.function_call.arguments)
        updated_ui = set_ui_values(**args)

        # Add the tool result back into the conversation
        messages.append({
            "role": "function",
            "name": "set_ui_values",
            "content": json.dumps(updated_ui)
        })

        # 2nd pass: get GPT’s natural-language response
        final = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final.choices[0].message.content

    # If no function call, just return GPT’s response
    return msg.content

if __name__ == "__main__":
    print(chat_with_agent("Switch the molecule tab to ‘analysis’ and set the correlation to 0.75."))
    # -> GPT will invoke set_ui_values with those overrides and then summarize the new UI state.
