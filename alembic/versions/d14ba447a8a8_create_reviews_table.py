"""create_reviews_table

Revision ID: d14ba447a8a8
Revises: 28147626d8eb
Create Date: 2026-02-24 19:33:29.205159

"""
from typing import Sequence, Union
from alembic import op


revision: str = 'd14ba447a8a8'
down_revision: Union[str, None] = '28147626d8eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE reviews (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
            score SMALLINT NOT NULL CHECK (score >= 1 AND score <= 10),
            body TEXT,
            spoiler BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE (user_id, game_id)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE reviews")