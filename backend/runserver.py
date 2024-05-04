from service import app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2222, debug=True, threaded=True)
