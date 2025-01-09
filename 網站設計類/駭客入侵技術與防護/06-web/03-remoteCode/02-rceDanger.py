from flask import Flask, request

app = Flask(__name__)

@app.route('/execute')
def execute():
    user_input = request.args.get('file', '')
    
    try:
        with open(user_input, 'r') as file:
            exec(file.read())  # 執行文件內容
        return "Executed successfully"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
