def make_id(s):

    if s is None:
        s = ""

    s = s.lower()

    try:
        # Example : delete what's after the before the dot in
        # 'I. Probabilistic Vocabulary'
        s = s.split(".")[1]
    except:
        pass

    return s.strip().replace(" ", "_")
