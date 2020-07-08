import pandas as pd
from pathlib import Path


def read_txts_into_dataframe():
    df = pd.DataFrame(columns=["file", "text"])

    pathlist = Path("data/txts").glob("**/*.txt")
    i = 0
    for path in pathlist:
        txt_file = str(path)
        file_name = txt_file.split("/")[-1].split(".")[0]
        with open(txt_file, "r") as f:
            df.loc[i] = [file_name, f.read()]
        i += 1
    return df


def write_df_to_csv():
    read_txts_into_dataframe().to_csv("data/data.csv")


write_df_to_csv()
