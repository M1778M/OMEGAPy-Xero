from .syntax import official_assistant_formatting_v1
import random

class Assistant:
    prompts = ["You are a helpful assisnant.","You are an assistant.","You're the best assistant."]
    def get_random():
        return random.choice(Assistant.prompts)


available = {"Assistant":Assistant,"Interactive Assistant":official_assistant_formatting_v1}