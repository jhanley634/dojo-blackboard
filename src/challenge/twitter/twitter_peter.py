# from https://github.com/PeterTheobald/HackerDojoPythonGroup/blob/main/challenges/twitter.py

###
# based on the Leet challenge: https://leetcode.com/problems/design-twitter/
# but slightly different.
# You can follow either this spec, or the Leetcode one
###

from collections import defaultdict
from dataclasses import dataclass
from operator import attrgetter


@dataclass
class Tweet:
    userid: int
    content: str
    timestamp: int

    def __repr__(self) -> str:
        return f"Tweet(u={self.userid}, t={self.timestamp}, c={self.content!r})"


tweets: list[Tweet] = []
user_tweets = defaultdict[int, list[int]](list)
followers = defaultdict[int, set[int]](set)


def follow(myid: int, to_follow_id: int) -> None:
    followers[myid].add(to_follow_id)


def unfollow(myid: int, to_unfollow_id: int) -> None:
    followers[myid].discard(to_unfollow_id)


def tweet(myid: int, content: str) -> int:
    tweet_id = len(tweets)
    tweet = Tweet(myid, content, tweet_id)
    tweets.append(tweet)
    user_tweets[myid].append(tweet_id)
    return tweet_id


def users_tweets(userid: int) -> list[Tweet]:
    idxs = user_tweets.get(userid, [])
    return [tweets[i] for i in idxs]


def timeline(myid: int, limit: int = 10) -> list[Tweet]:
    ids = set(followers.get(myid, set()))
    ids.add(myid)  # include own tweets
    pool: list[Tweet] = []
    for u in ids:
        pool.extend(users_tweets(u)[-limit:])
    pool.sort(key=attrgetter("timestamp"), reverse=True)
    return pool[:limit]


def test_timeline_basic(*, verbose: bool = False) -> None:
    tweets.clear()
    followers.clear()
    user_tweets.clear()

    # Users: 1, 2, 3
    follow(1, 2)
    follow(1, 3)
    follow(2, 3)

    # Tweets (timestamps increase automatically)
    t20 = tweet(2, "u2: hello")
    t30 = tweet(3, "u3: first")
    t21 = tweet(2, "u2: update")
    t31 = tweet(3, "u3: second")
    t10 = tweet(1, "u1: my own tweet")

    # Timeline for user 1 (follows 2 and 3 + self)
    tl1 = timeline(1, limit=10)
    if verbose:
        print("Timeline(1):", [(t.userid, t.timestamp, t.content) for t in tl1])
    # Basic checks
    assert len(tl1) <= 10
    assert tl1 == sorted(tl1, key=lambda x: x.timestamp, reverse=True)
    assert {t.userid for t in tl1} <= {1, 2, 3}

    # Unfollow 3; timeline should exclude user 3 tweets
    unfollow(1, 3)
    tl1_after = timeline(1, limit=10)
    if verbose:
        msg = "Timeline(1) after unfollow(3):"
        print(msg, [(t.userid, t.timestamp, t.content) for t in tl1_after])
    assert 3 not in {t.userid for t in tl1_after}

    # User 2 timeline (follows 3)
    tl2 = timeline(2, limit=5)
    if verbose:
        print("Timeline(2):", [(t.userid, t.timestamp, t.content) for t in tl2])
    assert {t.userid for t in tl2} <= {2, 3}

    # Edge: user with no follows and no tweets
    tl999 = timeline(999, limit=5)
    if verbose:
        print("Timeline(999) (no follows/tweets):", tl999)
    assert tl999 == []

    # Edge: limit smaller than available
    tl1_top3 = timeline(1, limit=3)
    if verbose:
        print("Timeline(1) top 3:", [(t.userid, t.timestamp, t.content) for t in tl1_top3])
    assert len(tl1_top3) == min(3, len([t20, t21, t30, t31, t10]))


if __name__ == "__main__":
    test_timeline_basic()
