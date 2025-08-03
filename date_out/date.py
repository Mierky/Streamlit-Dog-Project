import pandas as pd

def getDate():
    # citire fisiere
    df_traits = pd.read_csv("date_in/breed_traits.csv")
    df_rank = pd.read_csv("date_in/breed_rank.csv")
    df_descriptions = pd.read_csv("date_in/akc-data-latest.csv")

    # rezolvare spatiere incorecta a fisierului exportat
    df_traits = df_traits.applymap(lambda x: x.replace("\u00a0", " ") if isinstance(x, str) else x)

    # prelucrare dataframeuri
    df_traits_rank = pd.merge(left=df_traits, right=df_rank, on="Breed")
    df_traits_rank["Breed"] = df_traits_rank["Breed"].apply(lambda x: x.rstrip("s") if isinstance(x, str) else x)

    df_total_merged = pd.merge(left=df_traits_rank, right=df_descriptions, how="inner", on="Breed")
    coloane = list(df_total_merged.columns[:17]) + list(df_total_merged.columns[25:28]) + list(
        df_total_merged.columns[30:37])

    df = df_total_merged[coloane].copy(deep=True)
    df.to_csv("date_out/date.csv", index=False)

    # 4. Analiza valorilor lipsa
    print(df.info())
    print("\nNumăr valori lipsă per coloană:")
    missing_vals = df.isnull().sum()
    print(missing_vals)

    # 4. Analiza valorilor incorecte (valori de 0)
    print("\nValorile de 0 per coloană:")
    zero_vals = (df == 0).sum()
    print(zero_vals)

    #Gasire inregistrari cu valori 0
    print("\nInregistrari cu valori 0:")
    zero_rows = df[(df == 0).any(axis=1)]
    print(zero_rows)

    #Stergere inregistrari cu valori de 0
    df = df.drop(zero_rows.index)

    return df