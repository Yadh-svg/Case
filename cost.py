import tiktoken

class TokenCounter:
    def __init__(self):
        """
        Initialize the TokenCounter with the encoding of a specific GPT model.
        """
        self.encoding = tiktoken.encoding_for_model("gpt-5")
        # GPT-5 pricing (example, adjust as per official rates)
        self.input_cost_per_million = 1.25  # USD per 1M input tokens
        self.output_cost_per_million = 10.0 # USD per 1M output tokens

    def count_tokens(self, text):
        """
        Count the number of tokens in a given text.
        Returns both the count and token IDs.
        """
        token_ids = self.encoding.encode(text)
        return len(token_ids)

    def estimate_cost(self, input_tokens, output_tokens):
        """
        Estimate the GPT-5 API cost based on input and output tokens.
        """
        cost_input = (input_tokens / 1_000_000) * self.input_cost_per_million
        cost_output = (output_tokens / 1_000_000) * self.output_cost_per_million
        total_cost = cost_input + cost_output
        return cost_input, cost_output, total_cost