from module import Server

test_server = Server(__name__)

if __name__ == "__main__":
    test_server.run(debug=True, port=5000)