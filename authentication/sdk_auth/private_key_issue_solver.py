import json
import os

from dotenv import load_dotenv


def fix_private_key(key: str) -> str:
    # Split the key into 64-character chunks
    chunks = [key[i:i + 64] for i in range(0, len(key), 64)]

    # Join the chunks with '\n' between each two consecutive chunks
    fixed_key = '\n'.join(chunks)
    return f"-----BEGIN PRIVATE KEY-----\n{fixed_key}\n-----END PRIVATE KEY-----\n"


def get_json_key() -> str:
    json_file = "../../costs/pizza_do_bill.json"
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data["private_key"]


def find_difference(str1: str, str2: str) -> tuple:
    """Find the first difference between two strings."""
    min_length = min(len(str1), len(str2))
    for i in range(min_length):
        if str1[i] != str2[i]:
            return i, str1[i], str2[i]
    return None


def __main():
    load_dotenv()
    raw_key = os.environ["SDK_PRIVATE_KEY"]
    transformed_key = fix_private_key(raw_key)
    desired_key = get_json_key()
    transformed_key = transformed_key.replace('\n', "•")
    desired_key = desired_key.replace('\n', "•")
    are_keys_equal = transformed_key == desired_key
    if not are_keys_equal:
        diff_index, char1, char2 = find_difference(transformed_key, desired_key)
        print(f"Strings first differ at index {diff_index}: {char1} vs {char2}")
    print(transformed_key[1677:1700])
    print(desired_key[1677:1700])
    print(len(transformed_key))
    print(len(desired_key))


if __name__ == '__main__':
    __main()
