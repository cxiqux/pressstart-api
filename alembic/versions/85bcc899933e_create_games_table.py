"""create_games_table

Revision ID: 85bcc899933e
Revises: 0d32083321e6
Create Date: 2026-02-24 19:31:27.300554

"""
from typing import Sequence, Union
from alembic import op


revision: str = '85bcc899933e'
down_revision: Union[str, None] = '0d32083321e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE games (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            rawg_id INTEGER NOT NULL UNIQUE,
            title VARCHAR(255) NOT NULL,
            cover_url TEXT,
            genre VARCHAR(100),
            platform VARCHAR(100),
            release_year SMALLINT,
            cached_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE games")