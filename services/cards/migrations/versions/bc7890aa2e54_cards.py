"""cards

Revision ID: bc7890aa2e54
Revises: fc090b022f82
Create Date: 2025-05-28 23:48:17.598023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bc7890aa2e54'
down_revision: Union[str, None] = 'fc090b022f82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'cards',
        'pin',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'cvv',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'number',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=50),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'cardholder',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=250),
        existing_nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'cards',
        'cardholder',
        existing_type=sa.String(length=250),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'number',
        existing_type=sa.String(length=50),
        type_=sa.INTEGER(),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'cvv',
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False
    )
    op.alter_column(
        'cards',
        'pin',
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False
    )
    # ### end Alembic commands ###
