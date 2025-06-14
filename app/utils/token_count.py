import tiktoken

def count_tokens(text:str, enc_name="o200k_base", thresh=2):
    """
    Counts the number of tokens in the given text using the specified encoding and applies a threshold multiplier.

    Args:
        text (str): The input text to be tokenized and counted.
        enc_name (str, optional): The name of the encoding to use. Defaults to "o200k_base".
        thresh (float, optional): A multiplier applied to the token count. Defaults to 2.

    Returns:
        int: The rounded token count after applying the threshold multiplier.
    """
    enc = tiktoken.get_encoding(enc_name)
    cnt = len(enc.encode(text)) * thresh
    if cnt < 50:
        return 50
    else:
        print("Anzahl der Tokens im Skript: ", cnt)
        return round(cnt)
