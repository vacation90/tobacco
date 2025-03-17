from db import base, session, models

base.Base.metadata.drop_all(session.engine)
base.Base.metadata.create_all(session.engine)
