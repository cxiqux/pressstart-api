"""create_users_table

Revision ID: 0d32083321e6
Revises: 
Create Date: 2026-02-24 19:28:43.226103

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '0d32083321e6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            avatar_url TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE users")