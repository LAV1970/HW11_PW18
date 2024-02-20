from alembic import op
import sqlalchemy as sa
from alembic.migration import MigrationContext

# revision identifiers, used by Alembic.
revision = "c05514599a5a"
down_revision = None
branch_labels = None
depends_on = None


def has_table(table_name):
    context = MigrationContext.configure(op.get_bind())
    inspector = sa.inspect(context.connection)
    return inspector.has_table(table_name)


def has_index(index_name):
    """Check if an index with the given name exists."""
    context = MigrationContext.configure(op.get_bind())
    inspector = sa.inspect(context.connection)
    return index_name in inspector.get_indexes("contacts")


def create_table_if_not_exists():
    # Use raw SQL to check if the table "_alembic_tmp_contacts" exists before creating it
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS _alembic_tmp_contacts (
            id INTEGER NOT NULL,
            email VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR,
            phone_number VARCHAR,
            PRIMARY KEY (id)
        )
        """
    )


def upgrade():
    with op.batch_alter_table("contacts") as batch_op:
        # Drop index only if it exists
        if has_index("contacts_name"):
            batch_op.drop_index("contacts_name")

        batch_op.create_index(op.f("contacts_email"), ["email"], unique=False)
        batch_op.create_index(op.f("contacts_first_name"), ["first_name"], unique=False)
        batch_op.create_index(op.f("contacts_last_name"), ["last_name"], unique=False)
        batch_op.drop_column("name")
        batch_op.drop_column("phone")

    # Use raw SQL to create or replace the table "_alembic_tmp_contacts"
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS _alembic_tmp_contacts (
            id INTEGER NOT NULL,
            email VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR,
            phone_number VARCHAR,
            PRIMARY KEY (id)
        )
        """
    )

    # Create an intermediate step to avoid circular dependency
    with op.batch_alter_table("contacts") as batch_op:
        batch_op.add_column(sa.Column("first_name", sa.String(), nullable=True))

        # Continue with other modifications
        batch_op.add_column(
            sa.Column(
                "birthday",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.create_index(
            op.f("contacts_birthday"), "contacts", ["birthday"], unique=False
        )
