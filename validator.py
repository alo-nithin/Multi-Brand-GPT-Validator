import hashlib, json, os, re
from datetime import datetime
from dateutil import tz
from typing import Dict, List, Tuple

def _cfg_path(brand: str) -> str:
    return os.path.join("config", f"{brand.lower().replace(' ','')}.json")

def load_brand_config(brand: str) -> Dict:
    p = _cfg_path(brand)
    if not os.path.exists(p):
        raise FileNotFoundError(f"Config not found for brand: {brand}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def check_caption_rules(caption: str, rules: Dict) -> List[str]:
    errors = []
    max_chars = rules.get("max_chars", 99999)
    if len(caption) > max_chars:
        errors.append(f"CAPTION_TOO_LONG:{len(caption)}>{max_chars}")
    return errors

def check_forbidden_words(text: str, words: List[str]) -> List[str]:
    low = text.lower()
    hits = [w for w in words if w.lower() in low]
    return [f"FORBIDDEN_WORD:{w}" for w in hits]

def check_bank(values: List[str], bank: List[str], field: str) -> List[str]:
    if not bank: return []
    not_allowed = [v for v in values if v not in bank]
    return [f"{field.upper()}_NOT_ALLOWED:{v}" for v in not_allowed]

def check_media_policy(media: Dict, policy: Dict) -> List[str]:
    errors = []
    mtype = media.get("type")
    allowed = policy.get("allowed", [])
    if mtype not in allowed:
        errors.append(f"MEDIA_TYPE_NOT_ALLOWED:{mtype}")
    if mtype == "carousel":
        count = media.get("count", 0)
        maxc = policy.get("max_carousel", 10)
        if count < 1 or count > maxc:
            errors.append(f"CAROUSEL_COUNT_INVALID:{count}>{maxc}")
    return errors

def check_link_policy(links: List[Dict], policy: Dict) -> List[str]:
    errors = []
    allowed = [d.lower() for d in policy.get("allowed_domains", [])]
    for l in links:
        url = l.get("url","")
        domain = url.split("/")[2].lower() if "://" in url else url
        if not any(domain.endswith(ad) for ad in allowed):
            errors.append(f"LINK_DOMAIN_NOT_ALLOWED:{domain}")
    return errors

def apply_utm(url: str, brand: str, platform: str, week: str, tpl: str) -> str:
    if not tpl: return url
    sep = "&" if "?" in url else "?"
    utm = tpl.format(platform=platform.lower(), brand=brand.lower(), week=week)
    return f"{url}{sep}{utm}"

def sha256_of_bundle(bundle: Dict) -> str:
    data = json.dumps(bundle, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def iso_week_str(now: datetime, tz_name: str = "Europe/London") -> str:
    d = now.astimezone(tz.gettz(tz_name))
    return f"W{d.isocalendar().week:02d}"

def write_proof(brand_cfg: Dict, post_id: str, sha: str, ts: datetime) -> str:
    week = iso_week_str(ts, brand_cfg["proof_manifest"]["timezone"])
    root = brand_cfg["proof_manifest"]["root"]
    os.makedirs(root, exist_ok=True)
    fp = os.path.join(root, f"{week}.hash")
    record = {"post_id": post_id, "sha256": sha, "timestamp": ts.isoformat()}
    blob = {"brand": brand_cfg["brand"], "week": week, "posts": [record]}
    if os.path.exists(fp):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                blob = json.load(f)
        except Exception:
            blob = {"brand": brand_cfg["brand"], "week": week, "posts": []}
        blob["posts"].append(record)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(blob, f, ensure_ascii=False, indent=2)
    return fp

def validate(bundle: Dict) -> Tuple[bool, List[str], Dict]:
    # load brand
    cfg = load_brand_config(bundle["brand"])
    platform = bundle["platform"]
    errors: List[str] = []

    # platform enabled?
    if platform not in cfg.get("platforms", []):
        errors.append(f"PLATFORM_NOT_ENABLED:{platform}")

    # caption rules
    cap_rules = cfg["caption_rules"].get(platform, {})
    errors += check_caption_rules(bundle.get("caption",""), cap_rules)

    # forbidden words
    errors += check_forbidden_words(bundle.get("caption",""), cfg.get("forbidden_words", []))

    # hashtag / CTA banks (if provided)
    bank = cfg.get("hashtag_bank", {}).get(platform, [])
    errors += check_bank(bundle.get("hashtags", []), bank, "hashtag")
    ctabank = cfg.get("cta_bank", {}).get(platform, [])
    if bundle.get("cta"):
        errors += check_bank([bundle["cta"]], ctabank, "cta")

    # media policy
    media_policy = cfg.get("media_policy", {}).get(platform, {})
    errors += check_media_policy(bundle.get("media_suggestion", {}), media_policy)

    # links / domain
    errors += check_link_policy(bundle.get("links", []), cfg.get("link_policy", {}))

    # normalize & apply UTM
    normalized = dict(bundle)
    lp = cfg.get("link_policy", {})
    for l in normalized.get("links", []):
        if l.get("utm"):
            l["url"] = apply_utm(l["url"], cfg["brand"], platform, bundle.get("week") or "W00", lp.get("utm_template",""))

    ok = len(errors) == 0
    if not ok:
        return False, errors, {}

    sha = sha256_of_bundle(normalized)
    proof_file = write_proof(cfg, bundle.get("post_id","post"), sha, datetime.utcnow())
    return True, [], {"sha256": sha, "proof_file": proof_file, "normalized_bundle": normalized}
