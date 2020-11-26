from waitress import serve
from xmastree import create_app

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(create_app(), host='0.0.0.0', port=5000)