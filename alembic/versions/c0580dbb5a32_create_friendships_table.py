"""create_friendships_table

Revision ID: c0580dbb5a32
Revises: d14ba447a8a8
Create Date: 2026-02-24 19:34:03.024605

"""
from typing import Sequence, Union
from alembic import op


revision: str = 'c0580dbb5a32'
down_revision: Union[str, None] = 'd14ba447a8a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE friendship_status AS ENUM ('pending', 'accepted', 'blocked');

        CREATE TABLE friendships (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            requester_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            addressee_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            status friendship_status NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE (requester_id, addressee_id)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE friendships")
    op.execute("DROP TYPE friendship_status")