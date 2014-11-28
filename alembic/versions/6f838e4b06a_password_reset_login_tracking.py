"""Password reset & login tracking.

Revision ID: 6f838e4b06a
Revises: 3f086b765016
Create Date: 2014-11-14 14:22:05.399189

"""

# revision identifiers, used by Alembic.
revision = '6f838e4b06a'
down_revision = '3f086b765016'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password_reset_link',
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('link_id'),
    sa.UniqueConstraint('user_id')
    )
    op.add_column(u'user', sa.Column('activated_at', sa.DateTime(), nullable=True))
    op.add_column(u'user', sa.Column('last_login_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'user', 'last_login_at')
    op.drop_column(u'user', 'activated_at')
    op.drop_table('password_reset_link')
    ### end Alembic commands ###
