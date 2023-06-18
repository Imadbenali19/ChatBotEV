# message = '/get_started{"token":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIzIiwidXNlcm5hbWUiOiJjbGllbnQiLCJlbmFibGUiOnRydWUsImxvY2tlZCI6ZmFsc2UsInJvbGVzIjoiQ0xJRU5UIiwiZXhwIjoxNjg2MjExMzE2LCJpYXQiOjE2ODYxMjQ5MTZ9.Wos8_84kYt1jg4mRDJ8HoyU73uTC56_-CN-zl-rus39NWx9Xglz9p0KcNlFk3lc9hwRB0VP3XEEktB30JkNYpw"}'
# token_start_index = message.find('"token":"') + len('"token":"')
# token_end_index = message.find('"', token_start_index)
# token = message[token_start_index:token_end_index]
# token_parts = token.split(':')
# token_value = token_parts[0].strip("'")
# print(token_value)

message = "status of S230933_7343sdjfjsdf sidjfis"
token_start_index = message.find('status of ') + len('status of ')
token = message[token_start_index:]
print(token)
# import jwt

# # Your JWT token value
# jwt_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMyIsInVzZXJuYW1lIjoiaW1hZHNic2JlbmFsaXNic0BnbWFpbC5jb20iLCJlbmFibGUiOnRydWUsImxvY2tlZCI6ZmFsc2UsInJvbGVzIjoiQUdFTlQiLCJleHAiOjE2ODYxMjg4OTksImlhdCI6MTY4NjA0MjQ5OX0.c9U7fnbDoXFOsQ44Jq6-U9br8eBo6wulBrdPY_gw7FE-8N8bk7YS4yDgLVB9pr09PSZMxOfqyYDWwnwe_k9_HQ'
# secret_key=''
# # Decode the JWT token
# try:
#     decoded_token = jwt.decode(jwt_token,algorithms=['HS512'],verify=True,key=secret_key)

#     print(decoded_token)
# except jwt.ExpiredSignatureError:
#     # Handle expired token error
#     print('Token has expired.')
# # except jwt.InvalidTokenError:
# #     # Handle invalid token error
# #     print('Invalid token.')

# import jwt

# # Your JWT token value
# jwt_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMyIsInVzZXJuYW1lIjoiaW1hZHNic2JlbmFsaXNic0BnbWFpbC5jb20iLCJlbmFibGUiOnRydWUsImxvY2tlZCI6ZmFsc2UsInJvbGVzIjoiQUdFTlQiLCJleHAiOjE2ODYxMjg4OTksImlhdCI6MTY4NjA0MjQ5OX0.LYmmhKNf4vzc8imsTPcP9Q8A-0hIvePWzcCKh3GBOkamHVkXUrekJvWYQmjjO6fuAFjHNMBJmlS_0oFCcPeJ_g'

# # Decode the JWT token without verifying the secret key
# decoded_token = jwt.decode(jwt_token, options={'verify_signature': False})

# print(decoded_token)

# import json

# # The input string
# input_string = '/get_started{"token":"{"token":"imad"}"}'

# # Extract the nested JSON substring
# start_index = input_string.find('/get_started{"token":"{"token":"')
# print("yyyyy ",start_index)
# end_index = input_string.rfind('"}"}') + 2
# print("zzzzz ",end_index)
# nested_json = input_string[start_index:end_index]
# token = input_string.split('/get_started{"token":"{"token":"')
# print(token[1])


# # Extract the value
# value = token[1].split('"')[0]

# print(value)

# Parse the nested JSON and extract the value
# json_data = json.loads(nested_json)
# value = json_data.get('token')

# print(value)


# payload={'sub': '13', 'username': 'imadsbsbenalisbs@gmail.com', 'enable': True, 'locked': False, 'roles': 'AGENT', 'exp': 1686128899, 'iat': 1686042499}

# print(payload['username'])

# email = "imadsbsbenalisbs@gmail.com"

# if "@" in email:
#     username = email.split("@")[0]
#     print(username)
# else:
#     print("No @gmail.com found in the email.")


