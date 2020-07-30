import nltk
import numpy as np

def to_ans(ans):
    answers = []
    for note in ans["results"]["docs"]:
        answers.append({"doi": note["doi"],
                        "doc_score": note["doc_score"],
                        "doc_date": note["doc_date"],
                        "title": note["title"],
                        "sents": [sent[1] for sent in note["sentences"]]})
    return answers

def to_paper_info(row, abstags, i2b2tags, genericHeader):
    if len(row["authors"]) > 0:
        authors = [".".join([author['first'], author['last']]) for author in row["authors"]]
    else:
        authors = []

    abstract = nltk.tokenize.sent_tokenize(row['abstract'])

    return {"paper_id": row["paper_id"],
                "doi": row["doi"],
                "title": row["title"],
                "doc_date": row["doc_date"],
                "authors": authors,
                "summary": "",
                "abstract": {"text": abstract,
                             "tags": abstags},
                "bodyText": {"section_header":
                                 {"original": [para[0] for para in row["body_text"]],
                                  "generic": genericHeader, },
                             "text": [para[1] for para in row["body_text"]],
                             "tags": i2b2tags},
                "url": row["url"],
            }

def get_section(sents, title, abstract, bodytext, originalHeader):
    sent_section = []
    filtered_sents = []
    for sent in sents:
        sent = sent.strip()
        set = False
        if sent in title:
            continue
        for text in abstract:
            if sent in text:
                filtered_sents.append(sent)
                sent_section.append('Abstract')
                set = True
                break
        if set:
            continue
        for idx, text in enumerate(bodytext):
            if sent in text:
                filtered_sents.append(sent)
                sent_section.append(originalHeader[idx])
                set = True
                break
        if not set:
            filtered_sents.append(sent)
            sent_section.append("")

    return filtered_sents, sent_section



def to_general_ans(ans, row, abstag, i2b2tags, genericHeader):
    if len(row["authors"]) > 0:
        authors = [".".join([author['first'], author['last']]) for author in row["authors"]]
    else:
        authors = []

    abstract = nltk.tokenize.sent_tokenize(row['abstract'])
    bodytext = [para[1] for para in row["body_text"]]
    originalHeader = [para[0] for para in row["body_text"]]

    sents = [sent[1] for sent in ans["sentences"] if type(sent[1]) is str]
    sents, sent_section = get_section(sents, row["title"], abstract, bodytext, originalHeader)

    res = {"answer": {"score": ans["doc_score"],
                      "sents": sents,
                      "sent_section": sent_section},
           "paper_id": row["paper_id"],
           "doi": row["doi"],
           "title": row["title"],
           "doc_date": row["doc_date"],
           "authors": authors,
           "summary": "",
           "abstract": {"text": abstract,
                        "tags": abstag},
           "bodyText": {"section_header": {"original": originalHeader,
                                           "generic": genericHeader, #TODO: change to generic section header
                                            },
                        "text": bodytext,
                        "tags": i2b2tags},
           "url": row["url"],
           }
    return res

def to_similar(database, similars, db_abstags, db_i2b2ner, db_genericheader):
    if similars is None:
        return [{"paper_id": "",
                    "doi": "",
                    "title": "",
                    "doc_date": "",
                    "authors": [""],
                    "summary": "",
                    "abstract": {"text": [""],
                                 "tags": {"sciwing": [], "coda19": []}},
                    "bodyText": {"section_header": {"original": [],
                                           "generic": []}, #TODO: change to generic section header
                                 "text": [""],
                                 "tags": {"sciwingI2B2":{}}}
                    ,
                    "url": "",
                    }]
    res = []

    for id in similars:
        idx = database.loc[database['paper_id']==id].index
        if len(idx) < 1:
            continue
        row = database.iloc[idx[0]]
        abstract = nltk.tokenize.sent_tokenize(row['abstract'])
        if not row["paper_id"] or row["paper_id"] not in db_abstags:
            abstags = {"sciwing": [""] * len(abstract),
                       "coda19": [""] * len(abstract)}
        else:
            abstags = db_abstags[row["paper_id"]]

        if not row["paper_id"] or row["paper_id"] not in db_i2b2ner:
            i2b2tags = {"sciwingI2B2": {}}
        else:
            i2b2tags = db_i2b2ner[row["paper_id"]]

        if not row["paper_id"] or row["paper_id"] not in db_genericheader:
            genericHeader = [""] * len(row["body_text"])
        else:
            genericHeader = db_genericheader[row["paper_id"]]

        res.append(to_paper_info(row, abstags, i2b2tags, genericHeader))
    return res


def to_graph(database, graph, db_abstags, db_i2b2ner, db_genericheader):
    date2idx = {month: i for i, month in enumerate(graph['Xaxis'])}
    y2idx = {type:i for i, type in enumerate(graph['Yaxis']) }
    print(date2idx)
    print(y2idx)
    for x in graph['Xaxis']:
        for y in graph['Yaxis']:
            temp = []
            paper_ids = graph['values'][','.join([x,y])]['articles']
            paper_ids = list(set(paper_ids))
            print("After filtering", len(paper_ids))
            graph['values'][','.join([x, y])]['num'] = len(paper_ids)
            for id in paper_ids:
                idx = database.loc[database['paper_id']==id].index
                if len(idx) < 1:
                    print(id)
                row = database.iloc[idx[0]]

                if not row["paper_id"] or row["paper_id"] not in db_abstags:
                    abstags = {"sciwing": [""] * len(row["abstract"])}
                else:
                    abstags = db_abstags[row["paper_id"]]

                if not row["paper_id"] or row["paper_id"] not in db_i2b2ner:
                    i2b2tags = {"sciwingI2B2": {}}
                else:
                    i2b2tags = db_i2b2ner[row["paper_id"]]

                if not row["paper_id"] or row["paper_id"] not in db_genericheader:
                    genericHeader = [""] * len(row["body_text"])
                else:
                    genericHeader = db_genericheader[row["paper_id"]]

                temp.append(to_paper_info(row, abstags, i2b2tags, genericHeader))

            graph['values'][','.join([x, y])]['articles'] = temp

    graph['numbers'] = np.zeros((len(graph['Yaxis']), len(graph['Xaxis']))).tolist()
    for x in graph["Xaxis"]:
        for y in graph["Yaxis"]:
            graph['numbers'][y2idx[y]][date2idx[x]] = graph['values'][','.join([x,y])]['num']

    return graph