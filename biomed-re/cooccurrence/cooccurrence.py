import pickle
import pandas as pd
from tqdm import tqdm

df_train = pd.DataFrame()
df_ent = pd.DataFrame()


def update_co_count(co_count, ent1, ent2):
    """count number of cooccurences of two entities without using labels"""
    # check that both entity texts are strings
    if (not isinstance(ent1, str)) or (not isinstance(ent2, str)):
        print(f"Entity not a string: {ent1}, {ent2}")
        return
    if ent1 < ent2:
        e1 = ent1
        e2 = ent2
    elif ent2 < ent1:
        e1 = ent2
        e2 = ent1
    else:
        print(f"Neither entity string is smaller: {ent1}, {ent2}")
        return
    if e1 in co_count:
        if e2 in co_count[e1]:
            co_count[e1][e2] += 1
        else:
            co_count[e1][e2] = 1
    else:
        co_count[e1] = {}
        co_count[e1][e2] = 1


def update_ent_count(ent_count, ent):
    """count how many times an entity is mentioned in total"""
    if ent in ent_count:
        ent_count[ent] += 1
    else:
        ent_count[ent] = 1


# calculate occurrence and co-occurrence counts
co_count = {}
ent_count = {}
for idx, _, _ in tqdm(df_train.itertuples(index=False)):
    PMID, e1, e2 = idx.split(".")
    # entity IDs should be different
    if e1 == e2:
        continue
    df_pmid = df_ent.loc[df_ent["PMID"] == PMID, :]
    ent1 = df_pmid.loc[df_pmid["id"] == e1,
                       :]["text"].values[0]  # name of entity 1
    ent2 = df_pmid.loc[df_pmid["id"] == e2,
                       :]["text"].values[0]  # name of entity 2
    ent1 = ent1.lower()
    ent2 = ent2.lower()
    # entity text should be different
    if ent1 == ent2:
        continue
    update_ent_count(ent_count, ent1)
    update_ent_count(ent_count, ent2)
    update_co_count(co_count, ent1, ent2)
# save dict
pickle.dump(co_count, open("co_count_train.p", "wb"))
pickle.dump(ent_count, open("ent_count_train.p", "wb"))
