import os
from alembic import context
from sqlalchemy import create_engine
url = os.environ["DATABASE_URL"]
def run():
    eng = create_engine(url)
    with eng.connect() as c:
        context.configure(connection=c, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()
run()
