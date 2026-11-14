"""create items"""
revision = "0001"
down_revision = None
from alembic import op
import sqlalchemy as sa
def upgrade():
    op.create_table("items", sa.Column("id", sa.Integer, primary_key=True), sa.Column("name", sa.String(100), nullable=False))
    op.execute("insert into items (name) values ('server'),('database'),('network')")
def downgrade():
    op.drop_table("items")
