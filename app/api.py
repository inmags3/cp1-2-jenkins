from flask import Flask, jsonify, request

from app.calc import add, sub

app = Flask(__name__)


def _get_int(name: str) -> int:
    value = request.args.get(name, None)
    if value is None:
        raise ValueError(f"Missing param: {name}")
    return int(value)


@app.get("/sum")
def sum_route():
    try:
        a = _get_int("a")
        b = _get_int("b")
        return jsonify({"result": add(a, b)})
    except Exception:
        return jsonify({"error": "Invalid parameters"}), 400


@app.get("/sub")
def sub_route():
    try:
        a = _get_int("a")
        b = _get_int("b")
        return jsonify({"result": sub(a, b)})
    except Exception:
        return jsonify({"error": "Invalid parameters"}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
