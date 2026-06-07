"""Static file serving routes for the geotester web app."""

import os

from flask import send_from_directory


def register_static_routes(app, static_folder):
    """Register static file serving routes to the Flask app."""

    @app.route("/code")
    def serve_code():
        """Serve the code.html file."""
        return send_from_directory(static_folder, "code.html")

    @app.route("/<path:filepath>")
    def serve_static(filepath):
        """Serve static files with index.html as fallback."""
        file_path = os.path.join(static_folder, filepath)
        if os.path.isfile(file_path):
            return send_from_directory(static_folder, filepath)
        return send_from_directory(static_folder, "index.html")
