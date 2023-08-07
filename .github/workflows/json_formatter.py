def convert_json_key_to_single_line(json_key_path):
    with open(json_key_path, 'r') as f:
        json_key_content = f.read()

    # Remove newlines and escape double quotes
    single_line_json_key = json_key_content.replace('\n', '\\n').replace('"', '\\"')

    return single_line_json_key


def __main():
    # Replace 'path_to_json_key.json' with your actual JSON key file path
    json_key_path = 'omnichat-9a789-5322d25ae638.json'
    single_line_key = convert_json_key_to_single_line(json_key_path)
    print(single_line_key)


if __name__ == '__main__':
    __main()
