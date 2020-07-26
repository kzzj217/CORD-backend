def to_ans(ans):
    answers = []
    for note in ans["results"]["docs"]:
        answers.append({"doi": note["doi"],
                        "doc_score": note["doc_score"],
                        "doc_date": note["doc_date"],
                        "title": note["title"],
                        "sents": [sent[1] for sent in note["sentences"]]})
    return answers

def to_abstract(row, tags):
    ans = {"doi": row["doi"].values[0],
     "paper_id": row["paper_id"].values[0],
     "title": row["title"].values[0],
     "authors": [".".join([author['first'], author['last'][0]]) for author in row["authors"].values[0]],
     "text": row['abstract'].values[0].split(".")[:-1],
     "sciwingTags":tags["sciwing"]}
    return ans