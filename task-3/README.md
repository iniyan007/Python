# 🧩 Custom ORM (Object-Relational Mapper) in Python

## 📌 Overview

This project implements a **lightweight ORM (Object-Relational Mapper)** from scratch using Python. It allows developers to interact with a SQLite database using Python classes instead of writing raw SQL queries.

The ORM supports:

* Model definition using classes
* Automatic table creation
* CRUD operations
* Query building with method chaining
* Foreign key relationships
* Lazy loading of related data

---

## 🎯 Features

* ✅ Define database tables as Python classes
* ✅ Auto-generate `CREATE TABLE` SQL
* ✅ Perform CRUD operations (`save`, `delete`)
* ✅ Query using `.filter()`, `.order_by()`, `.all()`
* ✅ Foreign key relationships
* ✅ Lazy loading (`user.posts`)
* ✅ Method chaining for queries

---

## 🧠 Concepts Used

* Python **Metaclasses** (`__new__`)
* **Descriptor Protocol** (`__get__`, `__set__`, `__set_name__`)
* **SQLite3** (standard library)
* SQL (DDL + DML)
* Method chaining pattern

---

## 🏗️ Architecture

### 1. Field System

Fields define table columns using descriptors.

```python
class Field:
    def __init__(self, column_type, nullable=False, unique=False)
```

#### Types:

* `CharField(max_length)`
* `IntegerField()`
* `ForeignKey(to, related_name)`

---

### 2. Model Metaclass

Handles:

* Collecting fields
* Setting table name
* Creating reverse relationships

```python
class ModelMeta(type):
```

---

### 3. Base Model Class

All models inherit from `Model`.

Key methods:

* `create_table()`
* `save()`
* `delete()`
* `filter()`
* `get()`

---

### 4. QuerySet

Handles query building:

```python
User.filter(age__gte=25).order_by("-name").all()
```

Supports:

* Filtering (`__gte`)
* Ordering (ASC/DESC)
* SQL generation

---

### 5. Relationships

#### ForeignKey

```python
author = ForeignKey(User, related_name="posts")
```

#### Lazy Loading

```python
alice.posts
```

Executes query only when accessed.

---

## 🧾 Example Models

```python
class User(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=255, unique=True)
    age = IntegerField(nullable=True)

class Post(Model):
    title = CharField(max_length=200)
    author = ForeignKey(User, related_name="posts")
```

---

## ⚙️ Usage

### 1. Create Tables

```python
User.create_table()
Post.create_table()
```

**Generated SQL:**

```sql
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INTEGER
);
```

---

### 2. Insert Records

```python
alice = User(name="Alice", email="alice@example.com", age=30)
alice.save()
```

**SQL:**

```sql
INSERT INTO user (name, email, age) VALUES (?, ?, ?)
```

---

### 3. Create Related Records

```python
post1 = Post(title="Hello World", author=alice)
post1.save()
```

---

### 4. Query Data

```python
users = User.filter(age__gte=25).order_by("-name").all()
```

**SQL:**

```sql
SELECT * FROM user WHERE age >= 25 ORDER BY name DESC;
```

---

### 5. Lazy Loading (Reverse Relation)

```python
alice.posts
```

**SQL:**

```sql
SELECT * FROM post WHERE author_id = 1;
```

---

## 🧪 Sample Output

```
SQL: CREATE TABLE IF NOT EXISTS user ...
Table 'user' created.

SQL: INSERT INTO user ...
Record saved: User(id=4)

SQL: SELECT * FROM user WHERE age >= 25 ORDER BY name DESC;
[User(id=1), User(id=2), User(id=3), User(id=4)]

SQL: SELECT * FROM post WHERE author_id = 4;
[Post(id=2)]
```

---

## 🏁 Conclusion

This project demonstrates how ORMs like Django ORM or SQLAlchemy work internally by implementing:

* Field descriptors
* Metaclass-based model creation
* Query abstraction layer
* Lazy-loaded relationships
