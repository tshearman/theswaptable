from queries import generate_connection


def initialize_tables(eng):
    from model import reg
    reg.metadata.create_all(eng)


def initialize():
    eng = generate_connection()
    initialize_tables(eng)
