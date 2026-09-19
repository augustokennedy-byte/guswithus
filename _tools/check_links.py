#!/usr/bin/env python3
"""Check every outbound link in the Resource Center.

A dead link here means someone looking for a food pantry or a shelter bed hits a
404. This is the first thing the fortnightly refresh runs.

  python3 check_links.py <resources.json> [--json report.json]
"""
import json, sys, ssl, pathlib, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Sites that refuse automated requests but are fine in a real browser.
# Verified by hand; re-check by opening the URL if one starts failing differently.
# Verified by hand in a real browser on 2026-09-19. Re-open one in a browser
# before treating a new failure from these as real.
BOT_BLOCKED = ("score.org", "ssa.gov", "sba.gov", "irs.gov", "camba.org",
               "potsbronx.org", "nystateofhealth.ny.gov")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def probe(url, method):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        return r.status, r.geturl()


def check(item):
    url = item["url"]
    try:
        status, final = probe(url, "HEAD")
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):          # many servers refuse HEAD
            try:
                status, final = probe(url, "GET")
            except urllib.error.HTTPError as e2:
                status, final = e2.code, url
            except Exception as e2:
                return {**item, "status": "ERROR", "detail": str(e2)[:120]}
        else:
            status, final = e.code, url
    except Exception as e:
        return {**item, "status": "ERROR", "detail": str(e)[:120]}

    ok = status == 200
    if not ok and status in (403, 503) and any(d in url for d in BOT_BLOCKED):
        return {**item, "status": status, "verdict": "bot-blocked (fine in browser)"}
    return {**item, "status": status, "final": final,
            "verdict": "ok" if ok else "CHECK",
            "redirected": final.rstrip("/") != url.rstrip("/")}


def main():
    data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    seen, items = set(), []
    for c in data["cards"]:
        for a in c["acts"]:
            if a["kind"] == "go" and a["href"].startswith("http") and a["href"] not in seen:
                seen.add(a["href"])
                items.append({"url": a["href"], "card": c["name"], "cat": c["cat"]})

    print("checking %d unique links...\n" % len(items), file=sys.stderr)
    with ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(check, items))

    broken = [r for r in results if r.get("verdict") == "CHECK" or r["status"] == "ERROR"]
    moved = [r for r in results if r.get("redirected") and r.get("verdict") == "ok"]

    for r in sorted(broken, key=lambda x: str(x["status"])):
        print("  %-7s %s\n           %s" % (r["status"], r["card"], r["url"]))
        if r.get("detail"):
            print("           %s" % r["detail"])
    print("\n%d links | %d ok | %d need a look | %d redirected"
          % (len(results), sum(1 for r in results if r.get("verdict") == "ok"),
             len(broken), len(moved)))

    if "--json" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print("report -> %s" % out)


if __name__ == "__main__":
    main()
