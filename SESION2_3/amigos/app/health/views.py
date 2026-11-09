from .. import db
from . import health


@health.route("/", strict_slashes=False)
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "ok", "database": "ok"}, 200
    except Exception:
        return {"status": "error", "database": "error"}, 503