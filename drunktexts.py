from waitress import serve
from routes import app
import logging

serve(app, host='0.0.0.0', port=5000)
#logger = logging.getLogger('waitress')
#logger.setLevel(logging.INFO)