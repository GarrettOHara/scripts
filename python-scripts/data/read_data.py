df_tv = pd.read_csv(
    'tv_data.csv',
    sep='|',
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL,
    engine='python',
    on_bad_lines='skip'
)

print(df_tv.shape)
