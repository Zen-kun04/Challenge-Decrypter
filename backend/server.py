from flask import Flask, jsonify, request
from hashlib import sha1, sha256, sha512, md5
from urllib.parse import unquote
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app)

hash_types = {
    "SHA256": sha256,
    "SHA1": sha1,
    "SHA512": sha512,
    "MD5": md5
}

db = sqlite3.connect("database.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS match (password TEXT, hash TEXT, salt TEXT);")
db.commit()

def get_from_db(hash_str: str, salt: str = None):
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    if salt:
        fetch = cur.execute("SELECT password FROM match WHERE hash = ? AND salt = ?", (hash_str, salt))
    else:
        fetch = cur.execute("SELECT password FROM match WHERE hash = ?", (hash_str,))
    return fetch.fetchone()

def decrypt(data: dict):
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    hash_str = data.get("hash")
    salt = data.get("salt")
    hash_type = data.get("type")
    if hash_type not in hash_types or hash_str is None:
        return {"message": "Invalid decrypt"}
    hash_str = unquote(data.get("hash"))
    hash_type = unquote(data.get("type"))

    if salt is not None:
        salt = unquote(data.get("salt"))

    if data_in_db := get_from_db(hash_str, salt):
        return {"password": data_in_db[0]}

    hasher = hash_types[hash_type]

    with open("rockyou.txt", 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if salt:
                if hasher(line.encode() + salt.encode()).hexdigest() == hash_str or \
                hasher(hasher(line.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str or \
                hasher(hasher(salt.encode()).hexdigest().encode() + line.encode()).hexdigest() == hash_str:
                    cur.execute("INSERT INTO match (password, hash, salt) VALUES (?, ?, ?);", (line, hash_str, salt))
                    db.commit()
                    return {"password": line}
            elif hasher(line.encode()).hexdigest() == hash_str:
                cur.execute("INSERT INTO match (password, hash) VALUES (?, ?);", (line, hash_str))
                db.commit()
                return {"password": line}

        return {"message": "The password could not be found in rockyou"}

@app.route('/decrypt')
def decrypt_route():
    args = request.args
    data = {}

    if "hash" in args and (args["hash"].strip() != ''):
        data["hash"] = args["hash"]
    else:
        return jsonify({
            "message": "Please set a hash !"
        })
    if "salt" in args and (args["salt"].strip() != ''):
        data["salt"] = args["salt"]
    if "type" in args and (args["type"].strip() != ''):
        data["type"] = args["type"]
    else:
        print(args)
        return jsonify({
            "message": "Please set a hash type !"
        })

    return jsonify(decrypt(data))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)