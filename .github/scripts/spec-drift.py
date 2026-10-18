#!/usr/bin/env python3
# #1789: compare this repo's openapi.json with the served spec at
# https://dicompute.ai/openapi.json (the public contract's live copy) and
# print a compact drift summary for a PR comment. Exit codes:
#   0 = in sync (or drift reported on stdout)
#   2 = served side unreachable -- NEVER a failure: the site being down
#       must not block a PR, it is a notice.
#   1 = the repo's own spec is unreadable (a genuine red).
import json, sys, urllib.request

REPO_SPEC = "openapi.json"
SERVED_URL = "https://dicompute.ai/openapi.json"

def load_repo():
    with open(REPO_SPEC) as f:
        return json.load(f)

def load_served():
    req = urllib.request.Request(SERVED_URL, headers={"User-Agent": "dicompute-openapi-drift-check"})
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(f := res)

def paths_of(spec):
    return set((spec.get("paths") or {}).keys())

def main():
    try:
        repo = load_repo()
    except Exception as e:
        print(f"repo spec unreadable: {e}", file=sys.stderr)
        return 1
    try:
        served = load_served()
    except Exception as e:
        print(f"served spec unreachable ({e}); drift not measured", file=sys.stderr)
        return 2
    repo_paths, served_paths = paths_of(repo), paths_of(served)
    only_repo = sorted(repo_paths - served_paths)
    only_served = sorted(served_paths - repo_paths)
    changed = sorted(
        p for p in repo_paths & served_paths
        if json.dumps(repo["paths"][p], sort_keys=True) != json.dumps(served["paths"][p], sort_keys=True)
    )
    ver_repo = (repo.get("info") or {}).get("version")
    ver_served = (served.get("info") or {}).get("version")
    if not only_repo and not only_served and not changed and ver_repo == ver_served:
        print("IN_SYNC")
        return 0
    print(f"versions: repo={ver_repo} served={ver_served}")
    print(f"paths only in repo ({len(only_repo)}): {', '.join(only_repo[:20]) or '-'}")
    print(f"paths only served ({len(only_served)}): {', '.join(only_served[:20]) or '-'}")
    print(f"paths changed ({len(changed)}): {', '.join(changed[:20]) or '-'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
