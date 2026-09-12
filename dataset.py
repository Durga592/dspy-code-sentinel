import dspy

# Specialized Dataset for Security Code Auditing & Patching
TRAIN_DATA = [
    dspy.Example(
        code="import os\ndef run_cmd(user_input):\n    os.system('ls ' + user_input)",
        vulnerability="Command Injection (CWE-78)",
        risk_level="CRITICAL",
        patched_code="import subprocess\nimport shlex\ndef run_cmd(user_input):\n    subprocess.run(['ls', user_input], check=True)"
    ).with_inputs("code"),
    
    dspy.Example(
        code="import sqlite3\ndef get_user(username):\n    conn = sqlite3.connect('db.sq3')\n    cursor = conn.cursor()\n    cursor.execute(f'SELECT * FROM users WHERE name = \"{username}\"')",
        vulnerability="SQL Injection (CWE-89)",
        risk_level="CRITICAL",
        patched_code="import sqlite3\ndef get_user(username):\n    conn = sqlite3.connect('db.sq3')\n    cursor = conn.cursor()\n    cursor.execute('SELECT * FROM users WHERE name = ?', (username,))"
    ).with_inputs("code"),

    dspy.Example(
        code="import pickle\ndef load_data(raw_bytes):\n    return pickle.loads(raw_bytes)",
        vulnerability="Insecure Deserialization (CWE-502)",
        risk_level="HIGH",
        patched_code="import json\ndef load_data(raw_bytes):\n    return json.loads(raw_bytes.decode('utf-8'))"
    ).with_inputs("code")
]

VAL_DATA = [
    dspy.Example(
        code="def read_file(path):\n    with open('/var/www/uploads/' + path, 'r') as f:\n        return f.read()",
        vulnerability="Path Traversal (CWE-22)",
        risk_level="HIGH",
        patched_code="import os\ndef read_file(path):\n    base_dir = '/var/www/uploads/'\n    target_path = os.path.abspath(os.path.join(base_dir, path))\n    if not target_path.startswith(base_dir):\n        raise ValueError('Access Denied')\n    with open(target_path, 'r') as f:\n        return f.read()"
    ).with_inputs("code")
]
