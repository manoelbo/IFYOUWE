"""empty message

Revision ID: 4774e1e5e368
Revises: 23f7387134e9
Create Date: 2015-06-01 15:42:56.357891

"""

# revision identifiers, used by Alembic.
revision = '4774e1e5e368'
down_revision = '23f7387134e9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(u'registrations')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'registrations',
    sa.Column(u'supporter_id', sa.INTEGER(), nullable=True),
    sa.Column(u'supported_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['supported_id'], [u'projects.id'], ),
    sa.ForeignKeyConstraint(['supporter_id'], [u'users.id'], )
    )
    ### end Alembic commands ###
