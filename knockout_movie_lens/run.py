from app import app

def main():
    app.run(host=app.config["APP_HOST"], port=app.config["APP_PORT"])

if __name__ == '__main__':
    main()
