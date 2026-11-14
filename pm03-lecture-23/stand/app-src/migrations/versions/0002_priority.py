"""add items.priority"""
revision = "0002"
down_revision = "0001"
from alembic import op
import sqlalchemy as sa
def upgrade():
    op.add_column("items", sa.Column("priority", sa.Integer, nullable=False, server_default="0"))
def downgrade():
    op.drop_column("items", "priority")
