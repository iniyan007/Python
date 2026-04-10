# 📘 Automated Testing Framework

---

# 🧠 Overview

This project implements a **lightweight automated testing framework** in Python that mimics core features of modern tools like pytest.

It supports:

* Test discovery
* Fixtures (dependency injection)
* Parameterized tests
* Skipping tests
* Parallel execution
* Structured result reporting

---

# 🎯 Objective

To build a system that can:

✔ Automatically discover test functions
✔ Execute them efficiently (parallel support)
✔ Inject dependencies using fixtures
✔ Handle multiple test inputs (parameterization)
✔ Provide clear output (pass/fail/skip with timing)

---

# 🏗️ System Architecture

```text
CLI → Test Discovery → Parameter Expansion → Fixture Injection
     → Execution Engine → Result Collection → Reporting
```

---

## 1️⃣ Test Discovery (`discover_tests`)

### 📌 Purpose:

Automatically find test functions inside test files.

### ⚙️ How it works:

* Scans directory using `os.listdir()`
* Imports modules dynamically using `importlib`
* Uses `dir()` to list attributes
* Uses `getattr()` to access objects
* Filters:

  * `callable(obj)` → must be a function
  * `hasattr(obj, "_is_test")` → must be marked with `@test`

### 🔁 Parameter Handling:

If function has `_params`, it expands into multiple test cases.

---

## 2️⃣ Decorators (`decorators.py`)

### 🔹 `@test`

Marks a function as a test:

```python
func._is_test = True
```

---

### 🔹 `@skip(reason)`

Skips execution:

```python
func._skip = True
func._skip_reason = reason
```

---

### 🔹 `@parametrize`

Allows multiple input combinations:

```python
@parametrize("x,y", [(1,2), (2,3)])
```

Internally stored as:

```python
func._params = [{"x":1,"y":2}, {"x":2,"y":3}]
```

---

## 3️⃣ Fixtures (`fixtures.py`)

### 📌 Purpose:

Provide reusable inputs to test functions.

---

### 🔹 Define fixture:

```python
@fixture()
def sample_data():
    return 10
```

---

### 🔹 Injection:

```python
def test_func(sample_data):
```

Framework:

* Inspects function parameters using `inspect.signature`
* Matches parameter names with fixture names
* Calls fixture and injects value

---

### 🧠 Concept:

👉 **Dependency Injection**

---

## 4️⃣ Test Execution (`runner.py`)

### Function:

```python
run_single_test(test_func, param, verbose)
```

---

### ⚙️ Flow:

1. Check if skipped
2. Start timer
3. Resolve fixtures
4. Apply parameters
5. Execute test
6. Handle exceptions

---

### 🧨 Exception Handling:

| Exception       | Result |
| --------------- | ------ |
| AssertionError  | FAIL   |
| Other Exception | ERROR  |
| No error        | PASS   |

---

### 📤 Output Format:

```python
("PASS", name, message, duration)
```

---

## 5️⃣ Parallel Execution (`multiprocessing.Pool`)

### 📌 Purpose:

Speed up execution using multiple CPU cores

---

### Implementation:

```python
with Pool(workers) as p:
    results = p.starmap(run_single_test, test_cases)
```

---

### 🧠 Working:

* Distributes tests across processes
* Executes simultaneously
* Collects results

---

## 6️⃣ CLI Interface (`argparse`)

### Command:

```bash
python minitest.py run tests --parallel 4 --verbose
```

---

### Arguments:

| Argument     | Description       |
| ------------ | ----------------- |
| `command`    | Action (run)      |
| `path`       | Test directory    |
| `--parallel` | Number of workers |
| `--verbose`  | Detailed output   |

---

## 7️⃣ Result Reporting

### Function:

```python
print_results(results, verbose)
```

---

### Output Includes:

* Test name
* Status (PASS/FAIL/SKIP)
* Execution time
* Error message (if any)

---

### Summary:

```text
6 tests | 5 passed | 0 failed | 1 skipped
Total time: 0.01s
```

---

# 🧪 Example Test Case

```python
@test
@parametrize("x,y", [(1,2), (2,3)])
def test_add(x, y):
    assert x + 1 == y
```

---

# 🔄 Execution Flow

```text
User runs CLI
        ↓
Tests discovered from files
        ↓
Decorators identify valid tests
        ↓
Parameters expanded
        ↓
Fixtures injected
        ↓
Tests executed (parallel)
        ↓
Results collected
        ↓
Summary printed
```

---

# 🧠 Key Concepts Used

* Decorators (`@test`, `@fixture`, `@parametrize`)
* Introspection (`inspect`, `getattr`, `hasattr`)
* Dynamic imports (`importlib`)
* Parallel processing (`multiprocessing.Pool`)
* Exception handling (`try/except`)
* CLI parsing (`argparse`)

---

# 🚀 Features Implemented

✅ Test discovery
✅ Parameterized tests
✅ Fixture injection
✅ Skip functionality
✅ Parallel execution
✅ Execution timing
✅ Structured reporting

---

# 🎯 Conclusion

This project demonstrates how a testing framework works internally by combining:

* Python introspection
* Functional decorators
* Parallel execution
* Structured reporting

It provides a strong foundation for understanding real-world tools like pytest.
