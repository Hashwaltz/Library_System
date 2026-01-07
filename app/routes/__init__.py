def register_blueprints(app):
    from .auth import auth_bp
    from .admin import admin_bp
    from .librarian import librarian_bp
    from .public import public_bp
    # from .logs import logs_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(librarian_bp)
    # app.register_blueprint(logs_bp)
    app.register_blueprint(public_bp)

