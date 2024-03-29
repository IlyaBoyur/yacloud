"""01_initial-db

Revision ID: 2c2fa16ab567
Revises: 
Create Date: 2023-06-18 10:40:35.043843

"""
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2c2fa16ab567"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_created_at"), "user", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "userfile",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("path", sa.String(length=1024), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("is_downloadable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_userfile_created_at"),
        "userfile",
        ["created_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_userfile_created_at"), table_name="userfile")
    op.drop_table("userfile")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_index(op.f("ix_user_created_at"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
