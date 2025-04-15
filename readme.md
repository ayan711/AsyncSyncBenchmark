# 🔥 Performance Testing FastAPI with ApacheBench (ab)

This document guides you through using **ApacheBench (`ab`)** to benchmark a FastAPI API endpoint, especially to compare performance between **async** and **sync** routes.

---

## 🚀 Purpose

Simulate concurrent HTTP requests to a FastAPI endpoint and measure:

- Request throughput
- Response time under load
- Handling of concurrent users
- Performance impact of async vs sync logic

---

## 🧪 Test Command

```bash
ab -n 100 -c 100 http://127.0.0.1:8000/async-call
```

### Parameters Explained

| Flag     | Description                                                 |
| -------- | ----------------------------------------------------------- |
| `-n 100` | Total number of requests to perform                         |
| `-c 10`  | Number of concurrent requests (simulates 100 users at once) |
| URL      | Target FastAPI endpoint to test                             |

---

## ⚙️ Setup Instructions

### 1. ✅ Install ApacheBench

#### On Ubuntu/Debian:

```bash
sudo apt-get install apache2-utils
```

#### On macOS (Homebrew):

```bash
brew install httpd
```

#### On Windows:

Use WSL or download [Apache binaries](https://www.apachelounge.com/download/).

---

### 2. ✅ Run FastAPI App

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### 3. ✅ Run ApacheBench

```bash
ab -n 100 -c 100 http://127.0.0.1:8000/async-call
```

💡 Use `127.0.0.1` instead of `localhost` to avoid potential socket errors.

---

## 📊 Sample Output Explained

```text
Concurrency Level:      10
Time taken for tests:   3.012 seconds
Complete requests:      100
Failed requests:        0
Requests per second:    33.20 [#/sec]
Time per request:       301.2 [ms] (mean)
```

| Field               | Meaning                                          |
| ------------------- | ------------------------------------------------ |
| Concurrency Level   | Number of requests made in parallel              |
| Time taken          | Total duration for all requests                  |
| Requests per second | Throughput — higher is better                    |
| Time per request    | Average time taken per request (lower is better) |
| Failed requests     | Should be 0 — or your app may be crashing        |

---

## 🧠 Notes: Sync vs Async Performance

### 🔍 Observation:

```bash
ab -n 100 -c 100 http://127.0.0.1:8000/async-call
```

Then compare with:

```bash
ab -n 100 -c 100 http://127.0.0.1:8000/sync-call
```

| Scenario                | Expected Outcome                    |
| ----------------------- | ----------------------------------- |
| Async + 100 concurrency | Completes in ~3 sec (I/O overlaps)  |
| Sync + 100 concurrency  | Takes ~30+ sec (each blocks others) |

### 💡 Recap:

- **Async = concurrent I/O**, but runs on one core.
- **Sync = blocking I/O**, every call waits for the previous.
- Async helps when you have:
  - High `-c` (concurrency)
  - I/O-bound workloads

---

## ⚙️ Behind the Scenes: Do Requests Use Different Cores?

### ❓ Does each FastAPI request use a different CPU core?

> **Not by default.**

### Why?

- Uvicorn is single-threaded, single-core by default.
- Async is **concurrent** but not **parallel**.

### ✅ To Use All Cores:

Use `gunicorn` with multiple workers:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

This:

- Spawns 4 processes → 4 CPU cores
- Each has its own async event loop

---

## ✅ Use Cases

- Compare **sync vs async** endpoints
- Test **I/O-heavy routes** (DB, external APIs, etc.)
- See how your app performs under **concurrent load**
- Catch failures under stress **before deploying**

---

## 🧠 Pro Tips

- Use higher `-n` and `-c` values for stress testing:
  ```bash
  ab -n 1000 -c 200 http://127.0.0.1:8000/async-call
  ```
- Combine with FastAPI logging/middleware to trace latency.
- Monitor memory and CPU usage during tests.

---

## 🧹 Cleanup

To stop the server:

```bash
Ctrl + C
```

---

## 📎 Related Tools

For more advanced load testing:

- [Locust](https://locust.io/)
- [k6](https://k6.io/)
- [wrk](https://github.com/wg/wrk)

---

Happy benchmarking 🚀
