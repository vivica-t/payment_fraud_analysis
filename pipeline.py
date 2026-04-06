import duckdb
import pandas as pd

DB_PATH = "db/transactions.duckdb"
CSV_PATH = "data/fraudTrain.csv"

def load_and_clean():
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)

    # rename columns with underscore format
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Parse timestamps
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    df["trans_date"] = df["trans_date_trans_time"].dt.date
    df["trans_hour"] = df["trans_date_trans_time"].dt.hour
    df["trans_month"] = df["trans_date_trans_time"].dt.to_period("M").astype(str)
    df["trans_day_of_week"] = df["trans_date_trans_time"].dt.day_name()

    # Clean up amount
    df["amt"] = df["amt"].astype(float)

    # Flag column rename for clarity
    df = df.rename(columns={"is_fraud": "is_fraud"})

    print(f"Loaded {len(df):,} transactions. Writing to DuckDB...")

    con = duckdb.connect(DB_PATH)
    con.execute("DROP TABLE IF EXISTS transactions")
    con.execute("CREATE TABLE transactions AS SELECT * FROM df")
    con.close()

    print("Done. Database ready at", DB_PATH)

if __name__ == "__main__":
    load_and_clean()
