from backend import app, db, guard, models
from backend.models import User

# with app.app_context():
#     db.create_all()
#     if db.session.query(User).filter_by(username='Yasoob').count() < 1:
#         db.session.add(User(
#             username='Yasoob',
#             password=guard.hash_password('strongpassword'),
#             roles='admin'
#         ))
#     db.session.commit()

app.run(host="0.0.0.0", port="5873")
