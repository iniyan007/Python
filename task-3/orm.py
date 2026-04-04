import sqlite3

conn = sqlite3.connect("orm.db")
cursor = conn.cursor()

class Field:
    def __init__(self, column_type, nullable=False, unique=False):
        self.column_type = column_type
        self.nullable = nullable
        self.unique = unique

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not self.nullable and value is None:
            raise ValueError(f"{self.name} cannot be NULL")
        instance.__dict__[self.name] = value


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class ForeignKey(Field):
    def __init__(self, to, related_name=None):
        super().__init__("INTEGER", nullable=False)
        self.to = to
        self.related_name = related_name

    def __set_name__(self, owner, name):
        self.name = name
        self.column_name = f"{name}_id"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        fk_id = instance.__dict__.get(self.column_name)
        if fk_id:
            return self.to.get(id=fk_id)
        return None

    def __set__(self, instance, value):
        if value is None:
            raise ValueError("ForeignKey cannot be None")

        if value.id is None:
            raise ValueError("Save the related object before assigning it")

        instance.__dict__[self.column_name] = value.id

class ReverseRelation:
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def __get__(self, instance, owner):
        return self.model.filter(**{f"{self.field_name}_id": instance.id}).all()

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        for attr_name, value in attrs.items():
            if isinstance(value, Field):
                fields[attr_name] = value

        attrs["_fields"] = fields
        attrs["_table"] = name.lower()

        new_class = super().__new__(cls, name, bases, attrs)

        # Wire up reverse relations on the target model
        for attr_name, value in fields.items():
            if isinstance(value, ForeignKey) and value.related_name:
                setattr(value.to, value.related_name, ReverseRelation(new_class, attr_name))

        return new_class

class QuerySet:
    def __init__(self, model):
        self.model = model
        self.conditions = []
        self.order = ""

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            if "__gte" in key:
                field = key.split("__")[0]
                self.conditions.append(f"{field} >= {value}")
            else:
                self.conditions.append(f"{key} = {repr(value)}")
        return self

    def order_by(self, field):
        direction = "ASC"
        if field.startswith("-"):
            field = field[1:]
            direction = "DESC"
        self.order = f"ORDER BY {field} {direction}"
        return self

    def all(self):
        where = ""
        if self.conditions:
            where = "WHERE " + " AND ".join(self.conditions)

        query = f"SELECT * FROM {self.model._table} {where} {self.order};"
        print("SQL:", query)

        cursor.execute(query)
        rows = cursor.fetchall()

        return [self.model(**dict(zip([col[0] for col in cursor.description], row))) for row in rows]

class Model(metaclass=ModelMeta):
    id = IntegerField(nullable=True)

    def __init__(self, **kwargs):
        for key, field in self._fields.items():
            if isinstance(field, ForeignKey):
                # Support both author=obj and author_id=1 forms
                if key in kwargs:
                    setattr(self, key, kwargs[key])  # goes through __set__, stores _id
                else:
                    fk_value = kwargs.get(f"{key}_id")
                    self.__dict__[f"{key}_id"] = fk_value
            else:
                setattr(self, key, kwargs.get(key))
        self.id = kwargs.get("id")

    @classmethod
    def create_table(cls):
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for name, field in cls._fields.items():
            if isinstance(field, ForeignKey):
                col = f"{name}_id INTEGER"
            else:
                col = f"{name} {field.column_type}"

            if not field.nullable:
                col += " NOT NULL"
            if field.unique:
                col += " UNIQUE"

            columns.append(col)

        query = f"CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)});"
        print("SQL:", query)
        cursor.execute(query)
        conn.commit()

        print(f"Table '{cls._table}' created.")

    def save(self):
        fields = []
        values = []

        for name, field in self._fields.items():
            if isinstance(field, ForeignKey):
                fields.append(f"{name}_id")
                values.append(self.__dict__.get(f"{name}_id"))
            else:
                fields.append(name)
                values.append(getattr(self, name))

        query = f"INSERT INTO {self._table} ({', '.join(fields)}) VALUES ({', '.join(['?'] * len(values))})"
        print("SQL:", query)

        cursor.execute(query, values)
        conn.commit()

        self.id = cursor.lastrowid
        print(f"Record saved: {self}")

    def delete(self):
        query = f"DELETE FROM {self._table} WHERE id = {self.id}"
        print("SQL:", query)

        cursor.execute(query)
        conn.commit()

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        results = cls.filter(**kwargs).all()
        return results[0] if results else None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

class User(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=255, unique=True)
    age = IntegerField(nullable=True)


class Post(Model):
    title = CharField(max_length=200)
    author = ForeignKey(User, related_name="posts")

User.create_table()
Post.create_table()

alice = User(name="Alice", email="alice1@example.com", age=30)
alice.save()

post1 = Post(title="Hello World", author=alice)
post1.save()

users = User.filter(age__gte=25).order_by("-name").all()
print(users)

print(alice.posts)