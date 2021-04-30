from app import create_app
import logging

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    port = 5000
    app.logger.setLevel(logging.INFO)
    app.run('', port=port)
