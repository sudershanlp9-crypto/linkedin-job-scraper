import os
import sys
import json
import subprocess
import threading
from datetime import datetime
from django.shortcuts import render
from django.http import FileResponse, Http404, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

_jobs: dict = {}


def index(request):
    return render(request, "scraper_app/index.html")


@csrf_exempt
def scrape(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    email    = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    keyword  = request.POST.get("keyword", "python developer").strip()
    location = request.POST.get("location", "").strip()
    pages    = int(request.POST.get("pages", "2"))

    if not email or not password:
        return JsonResponse({"error": "Email and password are required."}, status=400)

    job_id       = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename     = f"linkedin_report_{job_id}.xlsx"
    output_path  = os.path.join(str(settings.MEDIA_ROOT), filename)
    driver_path  = os.path.join(str(settings.BASE_DIR), "chromedriver.exe")
    script_path  = os.path.join(str(settings.BASE_DIR), "run_scraper.py")

    _jobs[job_id] = {"status": "running", "filename": None, "error": None, "keyword": keyword}

    os.makedirs(str(settings.MEDIA_ROOT), exist_ok=True)

    def _run():
        try:
            # ── Launch as a completely fresh Python process (no Django/thread baggage) ──
            cmd = [
                sys.executable,          # same python.exe that runs Django
                script_path,
                email, password, keyword,
                location, str(pages),
                output_path, driver_path,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,             # 10 min max
                cwd=str(settings.BASE_DIR),
            )

            # Parse last line of stdout as JSON
            output_lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
            if not output_lines:
                _jobs[job_id]["status"] = "error"
                _jobs[job_id]["error"]  = (result.stderr or "Scraper produced no output.")[:500]
                return

            try:
                data = json.loads(output_lines[-1])
            except json.JSONDecodeError:
                _jobs[job_id]["status"] = "error"
                _jobs[job_id]["error"]  = output_lines[-1][:500]
                return

            if "error" in data:
                _jobs[job_id]["status"] = "error"
                _jobs[job_id]["error"]  = data["error"]
            else:
                _jobs[job_id]["status"]   = "done"
                _jobs[job_id]["filename"] = filename
                _jobs[job_id]["count"]    = data.get("count", 0)

        except subprocess.TimeoutExpired:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"]  = "Scraper timed out after 10 minutes."
        except Exception as e:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"]  = str(e)

    threading.Thread(target=_run, daemon=True).start()
    return JsonResponse({"job_id": job_id})


def scrape_status(request, job_id):
    job = _jobs.get(job_id)
    if not job:
        return JsonResponse({"error": "Unknown job ID"}, status=404)
    return JsonResponse(job)


def download_report(request, filename):
    path = os.path.join(str(settings.MEDIA_ROOT), filename)
    if not os.path.exists(path):
        raise Http404("Report not found.")
    return FileResponse(open(path, "rb"), as_attachment=True, filename=filename)
