"""create_backlog_entries_table

Revision ID: 28147626d8eb
Revises: 85bcc899933e
Create Date: 2026-02-24 19:32:11.709949

"""
from typing import Sequence, Union
from alembic import op


revision: str = '28147626d8eb'
down_revision: Union[str, None] = '85bcc899933e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE backlog_status AS ENUM ('want', 'playing', 'done', 'dropped');

        CREATE TABLE backlog_entries (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
            status backlog_status NOT NULL,
            score SMALLINT CHECK (score >= 1 AND score <= 10),
            notes TEXT,
            hours_played INTEGER,
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE (user_id, game_id)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE backlog_entries")
    op.execute("DROP TYPE backlog_status")