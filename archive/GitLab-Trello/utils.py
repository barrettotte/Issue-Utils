import json, os

def get_pretty_json(jsonRaw, sort=False):
    return json.dumps(jsonRaw, indent=4, sort_keys=sort)

def read_file_json(file_path):
    with open(file_path, 'r') as f: return json.load(f)
    raise Exception("Could not read file at path {}", file_path)

def write_file_json(file_path, buffer):
    try:
        with open(file_path, 'w+') as f:
            f.write(get_pretty_json(buffer))
    except Exception: 
        print("File at {} could not be written", file_path)

def end_with(p,c): 
    return p + (c if p[-1] != c else "")

# https://github.com/kennethreitz/requests/issues/3013
def print_response(res):
    print('HTTP/1.1 {status_code}\n{headers}\n\n{body}'.format(
      status_code=res.status_code,
      headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
      body=res.content,
    ))

def print_request(req):
    print('HTTP/1.1 {method} {url}\n{headers}\n\n{body}'.format(
      method=req.method,
      url=req.url,
      headers='\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      body=req.body,
    ))