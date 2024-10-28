for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

@app.route("/a/rout")
def insert_person() -> None:
    tainted = flask.request.get_json()
    engine = create_engine(
        "postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"
    )
    connection = engine.connect()

    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    # ruleid: sqlalchemy-flask
    result = connection.execute(text("select username from users where " + tainted))

    result = connection.execute(
        # ruleid: sqlalchemy-flask
        sqlalchemy.sql.expression.text("select username from users where " + tainted)
    )

    # ok: sqlalchemy-flask
    session.query(MyClass).filter(f"foo={tainted}")  # runtime error

    # ok: sqlalchemy-flask
    db.session.query(MyClass).filter(f"foo={tainted}")  # runtime error

    query = text("SELECT * FROM your_table WHERE column = :value")
    # ok: sqlalchemy-flask
    result = connection.execute(query, value=tainted)

    # ok: sqlalchemy-flask
    result = connection.execute(
        "SELECT * FROM your_table WHERE column = :value", value=tainted
    )

    # ok: sqlalchemy-flask
    Blog.query.with_entities(Blog.blog_title).filter(
        Blog.blog_title.like("%" + tainted + "%")
    ).all()

    # ok: sqlalchemy-flask
    stmt = select(users_table).where(users_table.c.name == bindparam(tainted))

    t = (
        text("SELECT * FROM users WHERE id=:user_id")
        .bindparams(user=tainted)
        .columns(id=String, name=String)
    )

    # ok: sqlalchemy-flask
    connection.execute(t)

    connection.execute(
        select(users_table)
        .where(users_table.c.name == bindparam(tainted))
        # ruleid: sqlalchemy-flask
        .prefix_with(tainted)
    )

    connection.execute(
        select(users_table)
        .where(users_table.c.name == bindparam(tainted))
        # ruleid: sqlalchemy-flask
        .suffix_with(tainted)
    )

    connection.execute(
        select(users_table)
        # ruleid: sqlalchemy-flask
        .from_statement(tainted)
    )
