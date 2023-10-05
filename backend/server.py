from flask import Flask, jsonify, request
from hashlib import sha1, sha256, sha512, md5

app = Flask(__name__)

hash_types = {
    "SHA256": sha256,
    "SHA1": sha1,
    "SHA512": sha512,
    "MD5": md5
}



def decrypt(data: dict):
    hash_str = data.get("hash")
    salt = data.get("salt")
    hash_type = data.get("type")
    if hash_type not in hash_types or hash_str is None:
        return {"message": "Invalid decrypt"}

    hasher = hash_types[hash_type]

    with open("rockyou.txt", 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if salt:
                if hasher(line.encode() + salt.encode()).hexdigest() == hash_str or \
                hasher(hasher(line.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str:
                    return {"password": line}
            elif hasher(line.encode()).hexdigest() == hash_str:
                return {"password": line}

        return {"message": "The password could not be found in rockyou"}




@app.route('/decrypt')
def decrypt_route():
    args = request.args
    data = {}

    if "hash" in args:
        data["hash"] = args["hash"]
    if "salt" in args:
        data["salt"] = args["salt"]
    if "type" in args:
        data["type"] = args["type"]
    else:
        return jsonify({
            "message": "Please set a hash type !"
        })
    

    return jsonify(decrypt(data))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)