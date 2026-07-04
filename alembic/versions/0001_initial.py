"""Initial migration — teachers, rooms, groups, timetable

Revision ID: 0001
Revises: 
Create Date: 2026-03-12 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── teachers ──────────────────────────────────────────────────────────────
    op.create_table(
        "teachers",
        sa.Column("id",         sa.Integer(),     autoincrement=True, nullable=False),
        sa.Column("full_name",  sa.String(100),   nullable=False),
        sa.Column("subject",    sa.String(100),   nullable=False),
        sa.Column("email",      sa.String(150),   nullable=True),
        sa.Column("is_active",  sa.Boolean(),     nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_teachers_id",        "teachers", ["id"],        unique=False)
    op.create_index("ix_teachers_full_name",  "teachers", ["full_name"], unique=False)
    op.create_index("ix_teachers_email",      "teachers", ["email"],     unique=True)

    # ── rooms ─────────────────────────────────────────────────────────────────
    op.create_table(
        "rooms",
        sa.Column("id",         sa.Integer(),    autoincrement=True, nullable=False),
        sa.Column("name",       sa.String(50),   nullable=False),
        sa.Column("capacity",   sa.Integer(),    nullable=False),
        sa.Column("room_type",  sa.String(50),   nullable=False, server_default="dars"),
        sa.Column("is_active",  sa.Boolean(),    nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_rooms_id",   "rooms", ["id"],   unique=False)
    op.create_index("ix_rooms_name", "rooms", ["name"], unique=True)

    # ── groups ────────────────────────────────────────────────────────────────
    op.create_table(
        "groups",
        sa.Column("id",             sa.Integer(),    autoincrement=True, nullable=False),
        sa.Column("name",           sa.String(50),   nullable=False),
        sa.Column("student_count",  sa.Integer(),    nullable=False),
        sa.Column("course_year",    sa.Integer(),    nullable=False),
        sa.Column("specialization", sa.String(100),  nullable=True),
        sa.Column("is_active",      sa.Boolean(),    nullable=False, server_default="true"),
        sa.Column("created_at",     sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at",     sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_groups_id",   "groups", ["id"],   unique=False)
    op.create_index("ix_groups_name", "groups", ["name"], unique=True)

    # ── timetable ─────────────────────────────────────────────────────────────
    op.create_table(
        "timetable",
        sa.Column("id",          sa.Integer(),  autoincrement=True, nullable=False),
        sa.Column("teacher_id",  sa.Integer(),  nullable=False),
        sa.Column("room_id",     sa.Integer(),  nullable=False),
        sa.Column("group_id",    sa.Integer(),  nullable=False),
        sa.Column("day_of_week", sa.Integer(),  nullable=False),
        sa.Column("start_time",  sa.Time(),     nullable=False),
        sa.Column("end_time",    sa.Time(),     nullable=False),
        sa.Column("subject",     sa.String(100), nullable=False),
        sa.Column("created_at",  sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at",  sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["teachers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["room_id"],    ["rooms.id"],    ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["group_id"],   ["groups.id"],   ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id",    "day_of_week", "start_time", name="uq_room_day_time"),
        sa.UniqueConstraint("group_id",   "day_of_week", "start_time", name="uq_group_day_time"),
        sa.UniqueConstraint("teacher_id", "day_of_week", "start_time", name="uq_teacher_day_time"),
    )
    op.create_index("ix_timetable_id",         "timetable", ["id"],         unique=False)
    op.create_index("ix_timetable_teacher_id",  "timetable", ["teacher_id"], unique=False)
    op.create_index("ix_timetable_room_id",     "timetable", ["room_id"],    unique=False)
    op.create_index("ix_timetable_group_id",    "timetable", ["group_id"],   unique=False)


def downgrade() -> None:
    op.drop_table("timetable")
    op.drop_table("groups")
    op.drop_table("rooms")
    op.drop_table("teachers")
