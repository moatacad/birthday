"""empty message

Revision ID: 2dff2924ed53
Revises: 
Create Date: 2020-11-27 12:13:45.925261

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2dff2924ed53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'guest', 'state', ['guest_state'], ['state_id'])
    op.alter_column('state', 'state_name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_server_default=sa.text("''"))
    op.alter_column('tbl_state', 'state_name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_server_default=sa.text("''"))
    op.create_foreign_key(None, 'transaction', 'guest', ['guest_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.alter_column('tbl_state', 'state_name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_server_default=sa.text("''"))
    op.alter_column('state', 'state_name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_server_default=sa.text("''"))
    op.drop_constraint(None, 'guest', type_='foreignkey')
    # ### end Alembic commands ###
