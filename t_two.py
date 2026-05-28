def vote(votes):
    """
    Подсчет голосов

    """
    vote_count = {}
    for vote in votes:
        if vote in vote_count:
            vote_count[vote] += 1
        else:
            vote_count[vote] = 1

    max_count = 0
    most_frequent_vote = None
    for vote, count in vote_count.items():
        if count > max_count:
            max_count = count
            most_frequent_vote = vote

    return most_frequent_vote