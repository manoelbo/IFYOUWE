"""empty message

Revision ID: 200b298032f4
Revises: 4774e1e5e368
Create Date: 2015-06-01 15:46:13.238675

"""

# revision identifiers, used by Alembic.
revision = '200b298032f4'
down_revision = '4774e1e5e368'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('social_id', sa.String(length=64), nullable=True),
    sa.Column('facebook_id', sa.BigInteger(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('who', sa.String(length=64), nullable=True),
    sa.Column('what', sa.String(length=128), nullable=True),
    sa.Column('couse', sa.String(length=64), nullable=True),
    sa.Column('challenged_twitter', sa.String(length=64), nullable=True),
    sa.Column('background_color', sa.String(length=64), nullable=True),
    sa.Column('emoji1', sa.String(length=64), nullable=True),
    sa.Column('emoji2', sa.String(length=64), nullable=True),
    sa.Column('emoji3', sa.String(length=64), nullable=True),
    sa.Column('emoji4', sa.String(length=64), nullable=True),
    sa.Column('emoji5', sa.String(length=64), nullable=True),
    sa.Column('organization_url', sa.String(length=64), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('pledged_amount', sa.BigInteger(), nullable=True),
    sa.Column('viewers_counter', sa.BigInteger(), nullable=True),
    sa.Column('timestamp', sa.Date(), nullable=True),
    sa.Column('end_first_round', sa.Date(), nullable=True),
    sa.Column('end_second_round', sa.Date(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_end_first_round', 'projects', ['end_first_round'], unique=False)
    op.create_index('ix_projects_end_second_round', 'projects', ['end_second_round'], unique=False)
    op.create_index('ix_projects_timestamp', 'projects', ['timestamp'], unique=False)
    op.create_table('reports',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pledged_amount', sa.BigInteger(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('project_id', 'user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports')
    op.drop_index('ix_projects_timestamp', 'projects')
    op.drop_index('ix_projects_end_second_round', 'projects')
    op.drop_index('ix_projects_end_first_round', 'projects')
    op.drop_table('projects')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
    op.drop_index('ix_roles_default', 'roles')
    op.drop_table('roles')
    ### end Alembic commands ###
