from flask.cli import FlaskGroup
from backend import app, db, guard, models
from backend.models import User


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()

#app.run(host="0.0.0.0", port="5873")

# curl localhost:5873/pull -d '{"start_time": 500, "end_time": 1000}' -H 'Content-Type: application/json'