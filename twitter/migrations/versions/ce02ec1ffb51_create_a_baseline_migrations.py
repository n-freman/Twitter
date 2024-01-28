"""Create a baseline migrations

Revision ID: ce02ec1ffb51
Revises: 
Create Date: 2024-01-27 16:31:50.963805

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ce02ec1ffb51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('username', sa.String(length=120), nullable=False),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table('follow',
        sa.Column('follower_user_id', sa.Integer(), nullable=False),
        sa.Column('followee_user_id', sa.Integer(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['followee_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['follower_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('follower_user_id', 'followee_user_id')
    )
    op.create_table('profile',
        sa.Column('photo', sa.Text(), nullable=True),
        sa.Column('background_photo', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date_joined', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('tweet',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.String(length=240), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_edited', sa.DateTime(), nullable=True),
        sa.Column('quote_of', sa.Integer(), nullable=True),
        sa.Column('reply_to', sa.Integer(), nullable=True),
        sa.Column('previous_on_thread', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['previous_on_thread'], ['tweet.id'], ),
        sa.ForeignKeyConstraint(['quote_of'], ['tweet.id'], ),
        sa.ForeignKeyConstraint(['reply_to'], ['tweet.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('like',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tweet_id', sa.Integer(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'tweet_id')
    )
    op.create_table('media',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tweet_id', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poll',
        sa.Column('tweet_id', sa.Integer(), nullable=False),
        sa.Column('length', sa.Interval(), nullable=True),
        sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('tweet_id')
    )
    op.create_table('choice',
        sa.Column('poll_id', sa.Integer(), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(['poll_id'], ['poll.tweet_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('poll_id', 'number')
    )
    op.create_table('answer',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('poll_id', sa.Integer(), nullable=False),
        sa.Column('choice_number', sa.Integer(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['poll_id', 'choice_number'], ['choice.poll_id', 'choice.number'], ),
        sa.ForeignKeyConstraint(['poll_id'], ['poll.tweet_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id', 'poll_id', 'choice_number')
    )


def downgrade() -> None:
    op.drop_table('answer')
    op.drop_table('choice')
    op.drop_table('poll')
    op.drop_table('media')
    op.drop_table('like')
    op.drop_table('tweet')
    op.drop_table('profile')
    op.drop_table('follow')
    op.drop_table('users')

