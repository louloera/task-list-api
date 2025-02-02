"""Past changes did not work, made changes to connect one goal to many tasks

Revision ID: d9114478ac94
Revises: 037bf8604f70
Create Date: 2023-05-04 16:30:17.264342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9114478ac94'
down_revision = '037bf8604f70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    op.drop_column('goal', 'goal_title')
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    op.add_column('goal', sa.Column('goal_title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
