def init_security(app, db):
    """Initialize Flask-Security."""
    global user_datastore
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(app, user_datastore)