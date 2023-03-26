def get_dsn(
    scheme: str,
    host: str,
    port: int,
    database: int,
) -> str:
    return f"{scheme}://{host}:{port}/{database}"


# TODO: write a class to divide read & write calls between primary & replicas
