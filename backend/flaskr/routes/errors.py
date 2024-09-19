"""
Error controller
"""

from flask import jsonify


def setup(app):

    @app.errorhandler(404)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        })
        return (json, 404)
    

    @app.errorhandler(405)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        })
        return (json, 405)
    
    
    @app.errorhandler(422)
    def request_error(error):
        json = jsonify({
            "success": False,
            "error": 422,
            "message": "Badly formatted request"
        })
        return (json, 422)

    @app.errorhandler(500)
    def server_error(error):
        json = jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        })
        return (json, 500)
