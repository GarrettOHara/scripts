import logging
import json

# Assuming logger is configured for the example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sample_documents = [
    {
        "_attachments": "attachments/",
        "_etag": "\"2b00d971-0000-0800-0000-687e7e6d0000\"",
        "_rid": "DaRYAKaTFCnNAwAAAAAAAA==",
        "_self": "dbs/DaRYAA==/colls/DaRYAKaTFCk=/docs/DaRYAKaTFCnNAwAAAAAAAA==/",
        "customerId": "customerIdDisabled",
        "feedback": 1,
        "id": "fb99739b-ace2-47f6-baf8-849fe42c7421",
        "request": {
            "cache_key": "recommend_data_source:should_i_watch_jurassic_world_rebirth",
            "chat_history": [
                {
                    "inputs": {
                        "chat_input": "What movie I should watch",
                        "customerId": ""
                    },
                    "outputs": {
                        "chat_output": "You should watch The Prestige if you want a smart, twisty thriller that keeps you guessing until the end."
                    }
                }
            ],
            "chat_input": "Which flick should I watch Jurassic World rebirth?",
            "contextQuery": "Should I watch Jurassic World Rebirth?",
            "customerId": "customerIdDisabled",
            "id": "fb99739b-ace2-47f6-baf8-849fe42c7421",
            "intent": "recommend-data-source"
        },
        "response": {
            "chat_output": "If you're considering \"Jurassic World Rebirth,\" it's a good pick if you enjoy action-packed dinosaur adventures with a post-apocalyptic twist. The movie is set five years after Jurassic World Dominion and explores the challenges of the planet's ecology being largely inhospitable to dinosaurs. It features a strong cast including Scarlett Johansson and Mahershala Ali, and is directed by Gareth Edwards.\n\nKeep in mind its Tomatometer score is around 52%, so it might be a mixed-bag critically, but if you are a fan of the Jurassic franchise or dinosaur-themed films, it can be quite entertaining! 🦖🎬\n\nWould you like me to find info on some similar movies or other options too?",
            "done": True,
            "from_cache": False,
            "id": "fb99739b-ace2-47f6-baf8-849fe42c7421",
            "response_time_ms": {
                "cache_read": 1,
                "cache_write": 1,
                "llm": 4950,
                "middleware": 662,
                "total": 5614,
                "ttfb": 1334
            },
            "status_code": 200,
            "streamed": True,
            "timestamp": 1753120360
        },
        "timestamp": "2025-07-21T17:52:45.430332114Z",
        "_ts": 1753120365
    },
    {
        "customerId": "customerIdDisabled",
        "id": "4fec5fac-2719-4a65-982d-cccf2a86d350",
        "request": {
            "customerId": "customerIdDisabled",
            "chat_input": "What movie can I see tonight?",
            "chat_history": [
                {
                    "inputs": {
                        "chat_input": "What movie I should watch",
                        "customerId": ""
                    },
                    "outputs": {
                        "chat_output": "You should watch The Prestige if you want a smart, twisty thriller that keeps you guessing until the end."
                    }
                }
            ],
            "intent": "recommend-data-source",
            "contextQuery": "What movies are available to watch on July 21 2025?",
            "id": "4fec5fac-2719-4a65-982d-cccf2a86d350",
            "cache_key": "recommend_data_source:what_movies_are_available_to_watch_on_july_21_2025"
        },
        "response": {
            "id": "4fec5fac-2719-4a65-982d-cccf2a86d350",
            "chat_output": "Hey {user_name}! Looking for a movie to catch tonight in theaters? Here are three options currently playing:\n\n<card>\n- card_type: movie\n- vanity_id: i_know_what_you_did_last_summer_2025\n- title: I Know What You Did Last Summer\n- Theatrical Release Date: Friday July 18, 2025\n- MPAA Rating: R\n- Genre: Horror\n</card>\n\n<card>\n- card_type: movie\n- vanity_id: eddington\n- title: Eddington\n- Theatrical Release Date: Friday July 18, 2025\n- MPAA Rating: R\n- Genre: Comedy\n</card>\n\n<card>\n- card_type: movie\n- vanity_id: smurfs\n- title: Smurfs\n- Theatrical Release Date: Friday July 18, 2025\n- MPAA Rating: PG\n- Genre: Kids family\n</card>\n\nWhether you're in the mood for horror, comedy, or a family-friendly flick, there's something to suit you tonight! Want info on streaming options or other genres? Just ask! 🎬😊",
            "done": True,
            "timestamp": 1753120355,
            "status_code": 200,
            "response_time_ms": {
                "total": 4572,
                "middleware": 781,
                "llm": 3767,
                "cache_read": 22,
                "cache_write": 1,
                "ttfb": 1274
            },
            "from_cache": False,
            "streamed": True
        },
        "timestamp": "2025-07-21T17:52:39.588672906Z",
        "_rid": "DaRYAKaTFCnMAwAAAAAAAA==",
        "_self": "dbs/DaRYAA==/colls/DaRYAKaTFCk=/docs/DaRYAKaTFCnMAwAAAAAAAA==/",
        "_etag": "\"2b00d471-0000-0800-0000-687e7e670000\"",
        "_attachments": "attachments/",
        "_ts": 1753120359
    }
]

from typing import List, Dict, Any
import json
import logging

# Assuming logger is configured elsewhere
logger = logging.getLogger(__name__)

def truncate_chat_history(
    conversations_data: List[Dict[str, Any]], max_entries: int = 50
) -> List[Dict[str, str]]:
    """
    Trims and de-duplicates chat history, returning it in a format suitable
    for the 'conversation' parameter of the create_batch_task function.
    """
    unique_exchanges = {}
    logger.info(
        "truncate_chat_history: conversations_data: "
        + "\n"
        + json.dumps(conversations_data, indent=2)
        + "\n"
    )

    for conversation in conversations_data:
        # Top-level conversation of document
        input_content = conversation.get("request", {}).get("chat_input")
        output_content = conversation.get("response", {}).get("chat_output")

        if input_content and output_content:  # Checks for non-empty and non-None
            unique_exchanges[input_content] = {
                "user": input_content,
                "assistant": output_content,
            }

        # Chat history exchange
        chat_history = conversation.get("request", {}).get("chat_history", []) # Changed from conversation.get to conversation.get("request", {}).get
        for exchange in chat_history:
            chat_input = exchange.get("inputs", {}).get("chat_input")
            chat_output = exchange.get("outputs", {}).get("chat_output")

            # Skip empty or None exchanges
            if not chat_input or not chat_output:
                continue

            # Create a key based on the input to identify duplicate exchanges
            unique_exchanges[chat_input] = {
                "user": chat_input,
                "assistant": chat_output,
            }

    all_exchanges_list = list(unique_exchanges.values())
    # Take the most recent unique exchanges
    selected_exchanges = all_exchanges_list[-max_entries:]

    # Return the selected exchanges in the desired format
    return selected_exchanges

# Get the truncated and formatted chat history
formatted_history_for_batch = truncate_chat_history(sample_documents)

# Assuming MODEL_NAME is defined elsewhere
MODEL_NAME = "gpt-4o"

def create_batch_task(
    custom_id: str,
    system_prompt: str, # Renamed from system_content to align with a common convention
    conversation: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    Creates a standardized dictionary for a single Azure OpenAI batch task,
    including a full conversation history where each item in the list
    contains both user and assistant messages.
    """
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    for exchange in conversation:
        if "user" in exchange:
            messages.append({"role": "user", "content": exchange["user"]})
        if "assistant" in exchange:
            messages.append({"role": "assistant", "content": exchange["assistant"]})

    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/chat/completions",
        "body": {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 300,
        },
    }

print("--- Formatted History from truncate_chat_history ---")
print(json.dumps(formatted_history_for_batch, indent=2))

# Now, use this output with create_batch_task
final_batch_task_payload = create_batch_task(
    custom_id="movie_recommendation_batch_task",
    system_prompt="You are an AI assistant specialized in movie recommendations.",
    conversation=formatted_history_for_batch
)

print("\n--- Final create_batch_task Payload ---")
print(json.dumps(final_batch_task_payload, indent=2))
