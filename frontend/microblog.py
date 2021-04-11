from app import app
import os


# Run this command to run the applciation in DEBUG mode
# docker run -p 5000:5000 -e DEBUG=1 <image-name>  e.g. flask_app_dev

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,  debug=os.environ.get('DEBUG') == '1')