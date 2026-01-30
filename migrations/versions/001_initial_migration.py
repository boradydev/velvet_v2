"""initial migration

Revision ID: 648d45859b4d
Revises: 
Create Date: 2026-01-30 20:59:36.541212

"""
from typing import Sequence, Union

from alembic import op

from migrations.utils import sql

# revision identifiers, used by Alembic.
revision: str = '648d45859b4d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sql("001_upgrade.sql"))


def downgrade() -> None:
    op.execute(sql("001_downgrade.sql"))

