"""initial migrate

Revision ID: 1330af9b6e63
Revises: 
Create Date: 2024-11-10 14:12:38.033257

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1330af9b6e63"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_path"),
    )
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("hashed_password", sa.String(length=512), nullable=False),
        sa.Column("email", sa.String(length=30), nullable=True),
        sa.Column(
            "role",
            sa.Enum(
                "USER",
                "MENTOR",
                "EDITOR",
                "ADREEDER",
                "DEVELOPER",
                "ADMIN",
                "HR",
                name="role",
            ),
            nullable=False,
        ),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=256), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "course_developers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "course_id"),
    )
    op.create_table(
        "modules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.CHAR(length=8), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("mentor_id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("is_draft", sa.Boolean(), nullable=False),
        sa.CheckConstraint("duration_days > 0", name="positive_duration_days"),
        sa.CheckConstraint("number > 0", name="positive_module_number"),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["mentor_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "course_posts",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["modules.id"],
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.PrimaryKeyConstraint("post_id", "module_id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "THEORY",
                "PRACTICE",
                "ENTRANCE_CERTIFICATION",
                "FINAL_CERTIFICATION",
                name="eventtype",
            ),
            nullable=False,
        ),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["modules.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "event_contents",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["contents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.PrimaryKeyConstraint("event_id", "content_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("event_contents")
    op.drop_table("events")
    op.drop_table("course_posts")
    op.drop_table("modules")
    op.drop_table("course_developers")
    op.drop_table("tokens")
    op.drop_table("courses")
    op.drop_table("users")
    op.drop_table("posts")
    op.drop_table("contents")
    # ### end Alembic commands ###
