# Cleaned up version of data-loading.ipynb
import argparse, os, sys
from time import time
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main(params: argparse.Namespace):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.tb
    url = params.url
    batch_count = params.batch_count
    batch_size = 100000 or params.batch_size

    # Get the name of the file from url
    file_name = url.rsplit("/", 1)[-1].strip()
    if os.path.exists(file_name):
        print(f"{file_name} already exists. Skipping download.")
    else:
        # Download file from url
        print(f"Downloading {file_name} ...")
        os.system(f"wget -O {file_name} {url.strip()}")
    print("\n")

    # Create SQL engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # Read file
    if file_name.endswith(".parquet"):
        file = pq.ParquetFile(file_name)
        df_head = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=batch_size)
    else:
        print("Error only .parquet files allowed.")
        sys.exit()

    # Create the table
    df_head.head(0).to_sql(name=table_name, con=engine, if_exists="replace")

    # Insert values
    t_start = time()
    count = 0
    for batch in df_iter:
        count += 1

        batch_df = batch.to_pandas()

        print(f"inserting batch {count}...")

        b_start = time()
        batch_df.to_sql(name=table_name, con=engine, if_exists="append")
        b_end = time()

        print(f"inserted! time taken {b_end-b_start:10.3f} seconds.\n")

        if batch_count and count >= batch_count:
            break

    t_end = time()
    print(
        f"Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches."
    )


if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser(
        description="Loading data from .parquet file link to a Postgres database."
    )

    parser.add_argument("--user", help="Username for Postgres.")
    parser.add_argument("--password", help="Password to the username for Postgres.")
    parser.add_argument("--host", help="Hostname for Postgres.")
    parser.add_argument("--port", help="Port for Postgres connection.")
    parser.add_argument("--db", help="Database name for Postgres")
    parser.add_argument("--tb", help="Destination table name for Postgres.")
    parser.add_argument("--url", help="URL for .parquet file.")
    parser.add_argument(
        "--batch-count", help="number of batch for data loading", type=int
    )
    parser.add_argument("--batch-size", help="size of batch for data loading", type=int)

    args = parser.parse_args()
    main(args)
