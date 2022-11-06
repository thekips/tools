import os
import requests

cookies = {
    'tinyUUID': 'eyJpdiI6InBINm14aUxCcnVyaVdSQVljSmFBdVE9PSIsInZhbHVlIjoiWnc5cWtnSVRaK2M4dE1kZ2QyWlhaTVJpelh0QW1yQ2hNank1em5FQmZPbVIzMUlrc1huRGVCc1g1a3p0bDNJaldXdW45REthUHdoYzZRL0dLTzYvbHY3d05VRTFNVjAyOXZ0OVZrWkNpeGM9IiwibWFjIjoiYTVjNzA5M2FlODE5OWM0MGJiYTk5MTYxNzQ5NjliZGM5NWJmMmQ0MGFhZjcwYjgxZjYyZGVlY2ZlMTZmZWU0MiIsInRhZyI6IiJ9',
    'early-access': 'eyJpdiI6IkMzc29TakFwby9rd1lac2E1SlQ3N0E9PSIsInZhbHVlIjoiYkJkWHRGYmF3QVVQK01nTGJrT3E4NDFsTVJoUGlpOTBHZEtXcmdZMzg0Yjh0b3FHVWZ2anpaVmFMdldLRmJ6akJYWTY3bndtbkhZRGRyS0dwOExWQUJaUWtZdDMyNGFpSTZpQnRRcktHbEk9IiwibWFjIjoiNGM0YzFlODdlZWE1OGFkMjljN2MzYjZmZTc1OTdmZDExZDZiMGFjNzVlYmUxNDRjM2QyYzdmOGIwMGIzY2VjNyIsInRhZyI6IiJ9',
    'XSRF-TOKEN': 'eyJpdiI6IlJTUXRDYkxmK2NSNWo4eGpaVm1oZkE9PSIsInZhbHVlIjoiMnFDcm9VYTR4V0loU1g4a2p1Q2lCTGQyL0EwUXVrQ0oyUUdmMnlPaHhlRFZySml3cG9jSks2d1dmL3M5NW9qb3dqd01OcmFXUTRuRUduSmhWeEVDKzJlQ3hyQXNOeUduOHhTZ2x3ZENBbzBhRmFjQys4M1NkdzUwN2RtQnMzQXciLCJtYWMiOiIzNTY0YWY0ZDI0YTE3NjlkODBlOGJmODQzNjI2N2ZiMWUyNTNlNGNjMTI3ZGJmODNhYjQ5OTMxZDY2ODI5YjNhIiwidGFnIjoiIn0%3D',
    'tinyurl_session': 'eyJpdiI6IjhWcm5TZWJ2U2N1RDlXamZPTEk2TEE9PSIsInZhbHVlIjoiMFVzUmRFOFg3Y1NYL01XZzg5MnR2SlRSeFVmTFArcjhKV2hUcGExOTRuOWpPZ0RlcmJjNURuUEc4QlRKVTdwREN2NjZuVm96R2owWmhhZnlNZVdzY1k1dkRuZ0tHbHVGQnNSL0JOVVpja0Rob3FZclZuZk4rVUpXQXJwaVkrNEMiLCJtYWMiOiJlZjY4ZTIxNGNhNjRhYjQzOTg4YzFiZDFmM2U5ZTdkM2NjZWFjNWY1MTgyMjlmYTFkNTgzMTVlY2FmZmQ2ZTIyIiwidGFnIjoiIn0%3D',
}

headers = {
    'authority': 'tinyurl.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'tinyUUID=eyJpdiI6InBINm14aUxCcnVyaVdSQVljSmFBdVE9PSIsInZhbHVlIjoiWnc5cWtnSVRaK2M4dE1kZ2QyWlhaTVJpelh0QW1yQ2hNank1em5FQmZPbVIzMUlrc1huRGVCc1g1a3p0bDNJaldXdW45REthUHdoYzZRL0dLTzYvbHY3d05VRTFNVjAyOXZ0OVZrWkNpeGM9IiwibWFjIjoiYTVjNzA5M2FlODE5OWM0MGJiYTk5MTYxNzQ5NjliZGM5NWJmMmQ0MGFhZjcwYjgxZjYyZGVlY2ZlMTZmZWU0MiIsInRhZyI6IiJ9; early-access=eyJpdiI6IkMzc29TakFwby9rd1lac2E1SlQ3N0E9PSIsInZhbHVlIjoiYkJkWHRGYmF3QVVQK01nTGJrT3E4NDFsTVJoUGlpOTBHZEtXcmdZMzg0Yjh0b3FHVWZ2anpaVmFMdldLRmJ6akJYWTY3bndtbkhZRGRyS0dwOExWQUJaUWtZdDMyNGFpSTZpQnRRcktHbEk9IiwibWFjIjoiNGM0YzFlODdlZWE1OGFkMjljN2MzYjZmZTc1OTdmZDExZDZiMGFjNzVlYmUxNDRjM2QyYzdmOGIwMGIzY2VjNyIsInRhZyI6IiJ9; XSRF-TOKEN=eyJpdiI6IlJTUXRDYkxmK2NSNWo4eGpaVm1oZkE9PSIsInZhbHVlIjoiMnFDcm9VYTR4V0loU1g4a2p1Q2lCTGQyL0EwUXVrQ0oyUUdmMnlPaHhlRFZySml3cG9jSks2d1dmL3M5NW9qb3dqd01OcmFXUTRuRUduSmhWeEVDKzJlQ3hyQXNOeUduOHhTZ2x3ZENBbzBhRmFjQys4M1NkdzUwN2RtQnMzQXciLCJtYWMiOiIzNTY0YWY0ZDI0YTE3NjlkODBlOGJmODQzNjI2N2ZiMWUyNTNlNGNjMTI3ZGJmODNhYjQ5OTMxZDY2ODI5YjNhIiwidGFnIjoiIn0%3D; tinyurl_session=eyJpdiI6IjhWcm5TZWJ2U2N1RDlXamZPTEk2TEE9PSIsInZhbHVlIjoiMFVzUmRFOFg3Y1NYL01XZzg5MnR2SlRSeFVmTFArcjhKV2hUcGExOTRuOWpPZ0RlcmJjNURuUEc4QlRKVTdwREN2NjZuVm96R2owWmhhZnlNZVdzY1k1dkRuZ0tHbHVGQnNSL0JOVVpja0Rob3FZclZuZk4rVUpXQXJwaVkrNEMiLCJtYWMiOiJlZjY4ZTIxNGNhNjRhYjQzOTg4YzFiZDFmM2U5ZTdkM2NjZWFjNWY1MTgyMjlmYTFkNTgzMTVlY2FmZmQ2ZTIyIiwidGFnIjoiIn0%3D',
    'dnt': '1',
    'origin': 'https://tinyurl.com',
    'referer': 'https://tinyurl.com/app',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IlJTUXRDYkxmK2NSNWo4eGpaVm1oZkE9PSIsInZhbHVlIjoiMnFDcm9VYTR4V0loU1g4a2p1Q2lCTGQyL0EwUXVrQ0oyUUdmMnlPaHhlRFZySml3cG9jSks2d1dmL3M5NW9qb3dqd01OcmFXUTRuRUduSmhWeEVDKzJlQ3hyQXNOeUduOHhTZ2x3ZENBbzBhRmFjQys4M1NkdzUwN2RtQnMzQXciLCJtYWMiOiIzNTY0YWY0ZDI0YTE3NjlkODBlOGJmODQzNjI2N2ZiMWUyNTNlNGNjMTI3ZGJmODNhYjQ5OTMxZDY2ODI5YjNhIiwidGFnIjoiIn0=',
}

url = input('Input the url: ')
json_data = {
    'url': url,
    'domain': 'tinyurl.com',
    'alias': '',
    'tags': [],
    'errors': {
        'errors': {},
    },
    'busy': True,
    'successful': False,
}

response = requests.post('https://tinyurl.com/app/api/create', cookies=cookies, headers=headers, json=json_data)
res = response.json()['data'][0]['aliases'][0]['tiny_url']
os.system('echo %s | clip' % res)
print(res)