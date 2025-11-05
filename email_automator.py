import json

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            raw = file.read()
        return json.loads(raw)
    except FileNotFoundError as e:
        print("The file not found")
    except FileExistsError as e:
        print("The file does not exist")

def check_json_format(data):
    try:
        if isinstance(data, list):
            rows = []
            for item in data:
                if not isinstance(item, dict) or 'email' not in item:
                    print("The json format should be list of dict items")
                rows.append({
                        'email':item['email'], 
                        'name':item.get('name',''),
                        'status':item.get('status', 'rejected')
                        })
            return rows
    except Exception:
        print("The json format should be list of dict items")
        

data = read_json('emails.json')
verified_data = check_json_format(data)
