"""add_multi_currency_support

Revision ID: 225032fb9e20
Revises: 
Create Date: 2025-04-24 06:57:05.390237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '225032fb9e20'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns
    op.add_column('btc_prices', sa.Column('price', sa.Float(), nullable=True))
    op.add_column('btc_prices', sa.Column('currency', sa.String(), nullable=True))

    # Update existing rows to set currency as 'eur'
    op.execute("UPDATE btc_prices SET price = price_eur, currency = 'eur'")

    # Make columns not nullable
    op.alter_column('btc_prices', 'price', nullable=False)
    op.alter_column('btc_prices', 'currency', nullable=False)

    # Update constraint
    op.drop_constraint('unique_price_timestamp', 'btc_prices')
    op.create_unique_constraint('unique_price_time_currency', 'btc_prices', ['price_timestamp', 'currency'])

    # Drop old column
    op.drop_column('btc_prices', 'price_eur')



def downgrade() -> None:
    # First recreate the old column
    op.add_column('btc_prices', sa.Column('price_eur', sa.Float(), nullable=True))

    # Copy data back
    op.execute("UPDATE btc_prices SET price_eur = price WHERE currency = 'eur'")

    # Restore old constraint
    op.drop_constraint('unique_price_time_currency', 'btc_prices')
    op.create_unique_constraint('unique_price_timestamp', 'btc_prices', ['price_timestamp'])

    # Drop new columns
    op.drop_column('btc_prices', 'price')
    op.drop_column('btc_prices', 'currency')



