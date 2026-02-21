"""initial schema

Revision ID: a947a034e6e7
Revises:
Create Date: 2026-02-05 14:35:06.312864
"""

from alembic import op
import sqlalchemy as sa

revision = 'a947a034e6e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Internet packages
    op.create_table(
        'internet_packages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('mikrotik_profile', sa.String(), nullable=False),
    )

    # Malls
    op.create_table(
        'malls',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
    )

    # Routers
    op.create_table(
        'routers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('mall_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('host', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('api_port', sa.Integer(), nullable=False, server_default='8728'),
        sa.ForeignKeyConstraint(['mall_id'], ['malls.id'], name='fk_routers_mall_id'),
    )

    # Users (MAC-based)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('mall_id', sa.Integer(), nullable=False),
        sa.Column('mac_address', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['mall_id'], ['malls.id'], name='fk_users_mall_id'),
        sa.UniqueConstraint('mall_id', 'mac_address', name='uq_users_mall_mac'),
    )

    op.create_index('ix_users_mac_address', 'users', ['mac_address'])
    op.create_index('ix_users_mall_id', 'users', ['mall_id'])

    # Payments
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('package_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('method', sa.String(), nullable=False),
        sa.Column('reference', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_payments_user_id'),
        sa.ForeignKeyConstraint(['package_id'], ['internet_packages.id'], name='fk_payments_package_id'),
    )

    # Subscriptions
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('package_id', sa.Integer(), nullable=False),
        sa.Column(
            'start_date',
            sa.DateTime(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_subscriptions_user_id'),
        sa.ForeignKeyConstraint(['package_id'], ['internet_packages.id'], name='fk_subscriptions_package_id'),
    )


def downgrade():
    op.drop_table('subscriptions')
    op.drop_table('payments')
    op.drop_index('ix_users_mall_id', table_name='users')
    op.drop_index('ix_users_mac_address', table_name='users')
    op.drop_table('users')
    op.drop_table('routers')
    op.drop_table('malls')
    op.drop_table('internet_packages')
