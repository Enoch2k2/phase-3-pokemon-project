
def _find_by_name(cls, session, name):
    return session.query(cls).filter(cls.name == name).first()


def _all(cls, session):
    return session.query(cls).all()
