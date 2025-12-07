import os
import subprocess
import threading
from flask import Flask, send_from_directory, request, jsonify, redirect
from datetime import datetime

app = Flask(__name__, static_folder="static")

crawl_logs = []
crawl_lock = threading.Lock()
crawl_running = False
crawl_process = None


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


@app.route("/api/redis-ui-url")
def get_redis_ui_url():
    redis_ui_url = os.getenv("REDIS_UI_URL")
    return jsonify({"url": redis_ui_url} if redis_ui_url else {})


@app.route("/api/crawl", methods=["POST"])
def start_crawl():
    global crawl_logs, crawl_lock, crawl_running

    if crawl_running:
        return jsonify({"error": "Crawl already in progress"}), 400

    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    with crawl_lock:
        crawl_logs = []
        crawl_logs.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting crawl...\n")

    def run_crawl():
        global crawl_logs, crawl_running
        crawl_running = True
        process = None
        try:
            cmd = ["python", "crawler.py", url]

            if data.get("user_agent"):
                cmd.extend(["--user-agent", data["user_agent"]])
            if data.get("allowed_domain"):
                cmd.extend(["--allowed-domain", data["allowed_domain"]])
            if data.get("level") is not None:
                cmd.extend(["--level", str(data["level"])])
            if data.get("use_storage"):
                cmd.append("--use-storage")

            with crawl_lock:
                crawl_logs.append(f"Executing: {' '.join(cmd)}\n")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd="/app",
            )
            crawl_process = process

            with crawl_lock:
                crawl_logs.append("Running...\n")

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    with crawl_lock:
                        crawl_logs.append(line)

            returncode = process.returncode

            with crawl_lock:
                if returncode == 0:
                    crawl_logs.append(
                        f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Crawl completed successfully\n"
                    )
                else:
                    crawl_logs.append(
                        f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Crawl completed with exit code {returncode}\n"
                    )
        except Exception as e:
            import traceback

            with crawl_lock:
                crawl_logs.append(
                    f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {str(e)}\n"
                )
                crawl_logs.append(f"Traceback: {traceback.format_exc()}\n")
        finally:
            if process:
                try:
                    process.stdout.close()
                except:
                    pass
            crawl_running = False
            crawl_process = None

    thread = threading.Thread(target=run_crawl, daemon=True)
    thread.start()

    return jsonify({"message": "Crawl started"})


@app.route("/api/logs")
def get_logs():
    global crawl_logs, crawl_lock, crawl_running

    with crawl_lock:
        logs = "".join(crawl_logs)

    status = "running" if crawl_running else "idle"
    if "Error:" in logs:
        status = "error"

    return jsonify({"logs": logs, "status": status})


@app.route("/api/clear-logs", methods=["POST"])
def clear_logs():
    global crawl_logs, crawl_lock

    with crawl_lock:
        crawl_logs = []

    return jsonify({"message": "Logs cleared"})


@app.route("/api/stop-crawl", methods=["POST"])
def stop_crawl():
    global crawl_running, crawl_process, crawl_logs, crawl_lock

    if not crawl_running:
        return jsonify({"error": "No crawl in progress"}), 400

    with crawl_lock:
        if crawl_process:
            try:
                crawl_process.terminate()
                crawl_process.wait(timeout=5)
            except:
                try:
                    crawl_process.kill()
                except:
                    pass
            crawl_logs.append(
                f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Crawl stopped by user\n"
            )

    crawl_running = False
    crawl_process = None

    return jsonify({"message": "Crawl stopped"})


@app.route("/redis-ui")
def redis_ui():
    redis_ui_url = os.getenv("REDIS_UI_URL")
    if redis_ui_url:
        return redirect(redis_ui_url)
    else:
        return jsonify({"message": "Redis UI not configured"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=debug)
