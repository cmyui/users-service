def get_dsn(
    scheme: str,
    host: str,
    port: int,
    database: int,
) -> str:
    return f"{scheme}://{host}:{port}/{database}"
