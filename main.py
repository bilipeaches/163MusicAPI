# 服务器
from flask import Flask, request
import api

app = Flask(__name__)
@app.route("/")
def main():
    return "服务器已启动!"

@app.route("/GetRes")
def GetRes():
    music_name = request.args.get("name")
    if music_name == None:
        return "你输入了个寂寞~"
    return str(api.GetRes(music_name))

@app.route("/GetLyric")
def GetLyric():
    id = request.args.get("id")
    if id == None:
        return "你输入了个寂寞~"
    return str(api.GetLyric(id))

if __name__ == "__main__":
    app.run(host="0.0.0.0")