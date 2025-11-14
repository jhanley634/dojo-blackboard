import unittest

from sqlalchemy import Engine, MetaData, Table

from src.challenge.twitter.schema import Base, get_engine


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
