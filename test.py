message = '/get_started{"token":"imadsdjfosdifoisoifzeorjziejrosizkokorko"}'
token_start_index = message.find('"token":"') + len('"token":"')
token_end_index = message.find('"', token_start_index)
token = message[token_start_index:token_end_index]
token_parts = token.split(':')
token_value = token_parts[0].strip("'")
print(token_value)
