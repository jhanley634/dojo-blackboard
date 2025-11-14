from challenge.twitter.twitter_pete import Implementation


def init() -> None: ...


def tweet(my_id: int, content: str) -> int:
    assert my_id > -1
    assert content
    return 0


def follow(my_id: int, to_follow_id: int) -> None: ...


def unfollow(my_id: int, to_unfollow_id: int) -> None: ...


_impl = Implementation(init, tweet, follow, unfollow)
