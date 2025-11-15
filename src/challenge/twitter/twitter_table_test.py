import unittest
from typing import TYPE_CHECKING

from sqlalchemy import Engine, MetaData, Table

from challenge.twitter.schema import Base, Tweet, User, get_engine, get_session
from challenge.twitter.twitter_table import follow, get_news_feed, init, tweet, unfollow

if TYPE_CHECKING:
    from challenge.twitter.twitter_pete import UserId


class TwitterSchemaTest(unittest.TestCase):
    engine: Engine | None = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = get_engine()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        Base.metadata.drop_all(cls.engine)

    def test_user_table_structure(self) -> None:
        metadata = MetaData()
        user_table = Table("user", metadata, autoload_with=self.engine)

        self.assertIn("id", [col.name for col in user_table.columns])

    def test_tweet_table_structure(self) -> None:
        metadata = MetaData()
        tweet_table = Table("tweet", metadata, autoload_with=self.engine)

        self.assertIn("id", [col.name for col in tweet_table.columns])
        self.assertIn("user_id", [col.name for col in tweet_table.columns])

    def test_follower_table_structure(self) -> None:
        metadata = MetaData()
        follower_table = Table("follower", metadata, autoload_with=self.engine)

        self.assertIn("follower_id", [col.name for col in follower_table.columns])
        self.assertIn("followee_id", [col.name for col in follower_table.columns])


class TwitterTableUnitTest(unittest.TestCase):

    def test_create_tweet(self) -> None:
        init()

        with get_session() as sess:
            alice: UserId = 0
            user = User(id=alice)
            sess.add(user)
            sess.commit()
            self.assertEqual([], get_news_feed(alice))

            tweet_id = tweet(alice, "Hello from Alice")
            self.assertEqual(1, tweet_id)
            result = sess.query(Tweet).filter_by(user_id=alice).first()
            assert result
            self.assertEqual(0, result.user_id)
            self.assertEqual("Hello from Alice", result.msg)
            self.assertEqual([1], get_news_feed(alice))
            unfollow(alice, alice)  # You can try, but unfollowing yourself has no effect.
            self.assertEqual([1], get_news_feed(alice))

            bob: UserId = 1
            sess.add(User(id=bob))
            sess.commit()
            self.assertEqual([], get_news_feed(bob))

            follow(bob, alice)
            self.assertEqual([1], get_news_feed(bob))

            unfollow(bob, alice)
            unfollow(bob, alice)  # Idempotent; doesn't matter if we actually were following.
            unfollow(bob, alice)
            self.assertEqual([], get_news_feed(bob))
