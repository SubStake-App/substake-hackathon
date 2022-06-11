import requests
import json
import dev_substrate_interface as dev

from flask import Flask, request, make_response, jsonify
app = Flask (__name__)

@app.route('/api/request/dev/collator', methods=['POST'])
def get_recommended_collator():
    if request.method == 'POST':
        
        return_str = json.dumps(dev.get_recommended_collators())
        
        response = make_response(return_str, 200)
        #print(return_str)
        return response
    else:
        return make_response("Not supported method", 400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)