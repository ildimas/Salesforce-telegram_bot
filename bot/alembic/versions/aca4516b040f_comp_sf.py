"""comp sf

Revision ID: aca4516b040f
Revises: f681f95fd4f5
Create Date: 2024-09-09 18:52:39.512340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aca4516b040f'
down_revision: Union[str, None] = 'f681f95fd4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('company_sf_id', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'companies', ['company_name'])
    op.create_unique_constraint(None, 'companies', ['company_sf_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_column('companies', 'company_sf_id')
    # ### end Alembic commands ###
