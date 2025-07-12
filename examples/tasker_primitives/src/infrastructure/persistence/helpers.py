from typing import Any

from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert


def build_upsert_statement(
    dialect_name: str, table: Table, values: dict[str, Any]
) -> Any:
    if dialect_name == "postgresql":
        insert_stmt = pg_insert(table)
    elif dialect_name == "sqlite":
        insert_stmt = sqlite_insert(table)
    else:
        raise NotImplementedError(f"Upsert not supported for {dialect_name}")

    print(f"Building upsert statement for dialect: {dialect_name}")

    columns = table.columns.keys()

    update_values = {
        k: getattr(insert_stmt.excluded, k)
        for k in values
        if k in columns and k != "id"
    }

    return insert_stmt.values(**values).on_conflict_do_update(
        index_elements=["id"], set_=update_values
    )
