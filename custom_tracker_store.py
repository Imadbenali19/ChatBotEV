from rasa.core.tracker_store import MongoTrackerStore

class CustomMongoTrackerStore(MongoTrackerStore):
    def __init__(self, domain, host, port, db_name, username, password, auth_source, collection):
        super().__init__(
            domain=domain,
            host=host,
            port=port,
            db_name=db_name,
            username=username,
            password=password,
            auth_source=auth_source,
            collection=collection
        )
