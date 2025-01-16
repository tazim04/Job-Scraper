from app import create_app
import sys
app = create_app()

if __name__ == '__main__':
    sys.stdout.reconfigure(line_buffering=True) # enable line buffering for stdout
    app.run(host='0.0.0.0', port=5000, debug=True) # allow access from outside the container