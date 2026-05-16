# -*- coding: utf-8 -*-
"""
PhishGuard AI - Phishing URL Detection Model Training
======================================================
Trains a Random Forest classifier to detect phishing URLs using 25
structural and lexical features extracted from each URL.

Dataset: datasets/new_data_urls.csv  (url, status columns)
  status=0 -> Legitimate
  status=1 -> Phishing

Features:
  Length-based     : url_length, domain_length, path_length
  Count-based      : num_dots, num_hyphens, num_underscores, num_slashes,
                     num_digits, num_params, num_fragments, num_subdomains,
                     num_special_chars
  Ratio-based      : digit_ratio, letter_ratio, special_char_ratio
  Boolean flags    : has_ip_address, has_at_symbol, has_double_slash_redirect,
                     has_https, is_shortened, has_suspicious_tld,
                     has_suspicious_keyword
  Entropy          : url_entropy (Shannon entropy)
  Domain tokens    : domain_token_count, longest_domain_token_len

Model: Random Forest Classifier (200 trees, max_depth=25)

Outputs -> backend/models/
  phishing_model.pkl   (trained model)
  vectorizer.pkl       (feature metadata)
"""

import os
import re
import sys
import math
import time
import warnings
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT_DIR / "datasets" / "new_data_urls.csv"
MODEL_DIR = ROOT_DIR / "backend" / "models"
MODEL_PATH = MODEL_DIR / "phishing_model.pkl"
FEATURE_META_PATH = MODEL_DIR / "vectorizer.pkl"

# ─────────────────────────────────────────────────────────────────────
# Known URL shorteners & suspicious TLDs / keywords
# ─────────────────────────────────────────────────────────────────────
SHORTENER_DOMAINS = {
    "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "su.pr", "db.tt",
    "qr.ae", "lnkd.in", "rb.gy", "cutt.ly", "shorturl.at", "v.gd",
    "rebrand.ly", "zpr.io",
}

SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".pw",
    ".cc", ".buzz", ".club", ".work", ".icu", ".cam", ".surf",
    ".rest", ".monster", ".quest",
}

SUSPICIOUS_KEYWORDS = {
    "login", "signin", "verify", "account", "update", "secure",
    "banking", "confirm", "password", "credential", "suspend",
    "unlock", "alert", "notification", "paypal", "apple", "microsoft",
    "amazon", "netflix", "support", "helpdesk", "service", "webscr",
    "ebayisapi", "wp-login", "admin", "authenticate",
}


# ─────────────────────────────────────────────────────────────────────
# Feature extraction helpers
# ─────────────────────────────────────────────────────────────────────
def shannon_entropy(s: str) -> float:
    """Shannon entropy of a string."""
    if not s:
        return 0.0
    prob = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in prob if p > 0)


def has_ip_pattern(url: str) -> int:
    """Return 1 if the URL uses an IP address instead of a hostname."""
    ip_pat = re.compile(
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    )
    hex_ip = re.compile(r"0x[0-9a-fA-F]{1,2}(?:\.0x[0-9a-fA-F]{1,2}){3}")
    return int(bool(ip_pat.search(url) or hex_ip.search(url)))


def extract_features(url: str) -> dict:
    """Extract 25 structural/lexical features from a URL string."""
    raw_url = url
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
    except Exception:
        parsed = urlparse("http://invalid.example.com")

    domain  = parsed.netloc.lower().split(":")[0]
    path    = parsed.path or ""
    query   = parsed.query or ""
    fragment = parsed.fragment or ""
    full    = raw_url.lower()

    # --- Length ---
    url_length    = len(raw_url)
    domain_length = len(domain)
    path_length   = len(path)

    # --- Counts ---
    num_dots        = full.count(".")
    num_hyphens     = full.count("-")
    num_underscores = full.count("_")
    num_slashes     = full.count("/")
    num_digits      = sum(c.isdigit() for c in full)
    num_params      = len(parse_qs(query))
    num_fragments   = 1 if fragment else 0
    num_special     = sum(
        not c.isalnum() and c not in (".", "/", ":", "-", "_") for c in full
    )
    domain_parts    = domain.split(".")
    num_subdomains  = max(0, len(domain_parts) - 2)

    # --- Ratios ---
    safe_len       = max(url_length, 1)
    digit_ratio    = num_digits / safe_len
    letter_ratio   = sum(c.isalpha() for c in full) / safe_len
    special_char_ratio = num_special / safe_len

    # --- Boolean flags ---
    has_ip                   = has_ip_pattern(raw_url)
    has_at                   = int("@" in raw_url)
    has_double_slash_redirect = int("//" in raw_url[8:]) if len(raw_url) > 8 else 0
    has_https                = int(raw_url.lower().startswith("https"))
    is_shortened             = int(domain in SHORTENER_DOMAINS)
    has_suspicious_tld       = int(any(domain.endswith(t) for t in SUSPICIOUS_TLDS))
    has_suspicious_keyword   = int(any(kw in full for kw in SUSPICIOUS_KEYWORDS))

    # --- Entropy ---
    url_entropy = shannon_entropy(raw_url)

    # --- Domain token stats ---
    domain_tokens          = re.split(r"[.\-_]", domain)
    domain_token_count     = len(domain_tokens)
    longest_domain_token   = max((len(t) for t in domain_tokens), default=0)

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "path_length": path_length,
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_underscores": num_underscores,
        "num_slashes": num_slashes,
        "num_digits": num_digits,
        "num_params": num_params,
        "num_fragments": num_fragments,
        "num_subdomains": num_subdomains,
        "num_special_chars": num_special,
        "digit_ratio": digit_ratio,
        "letter_ratio": letter_ratio,
        "special_char_ratio": special_char_ratio,
        "has_ip_address": has_ip,
        "has_at_symbol": has_at,
        "has_double_slash_redirect": has_double_slash_redirect,
        "has_https": has_https,
        "is_shortened": is_shortened,
        "has_suspicious_tld": has_suspicious_tld,
        "has_suspicious_keyword": has_suspicious_keyword,
        "url_entropy": url_entropy,
        "domain_token_count": domain_token_count,
        "longest_domain_token_len": longest_domain_token,
    }


FEATURE_NAMES = list(extract_features("http://example.com").keys())


# ─────────────────────────────────────────────────────────────────────
# Batch extraction with progress
# ─────────────────────────────────────────────────────────────────────
def extract_features_batch(urls: pd.Series) -> pd.DataFrame:
    total     = len(urls)
    milestone = max(1, total // 20)
    results   = []
    print(f"\n[*] Extracting features from {total:,} URLs ...")
    t0 = time.time()
    for i, url in enumerate(urls):
        results.append(extract_features(str(url)))
        if (i + 1) % milestone == 0:
            pct     = (i + 1) / total * 100
            elapsed = time.time() - t0
            rate    = (i + 1) / elapsed
            eta     = (total - i - 1) / rate
            print(f"    {pct:5.1f}%  ({i + 1:>8,} / {total:,})"
                  f"  [{elapsed:.0f}s elapsed, ~{eta:.0f}s left]")
    elapsed = time.time() - t0
    print(f"    [DONE] {total:,} URLs in {elapsed:.1f}s"
          f"  ({total / elapsed:,.0f} URLs/sec)\n")
    return pd.DataFrame(results, columns=FEATURE_NAMES)


# ─────────────────────────────────────────────────────────────────────
# Main training pipeline
# ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print("  PhishGuard AI  --  Phishing URL Detection Training")
    print("=" * 65)

    # ── 1. Load dataset ──────────────────────────────────────────────
    print(f"\n[1/7] Loading dataset: {DATASET_PATH}")
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATASET_PATH)
    print(f"      Rows: {len(df):,}   Columns: {list(df.columns)}")

    assert "url"    in df.columns, "Dataset must have a 'url' column"
    assert "status" in df.columns, "Dataset must have a 'status' column"

    initial_len = len(df)
    df.dropna(subset=["url", "status"], inplace=True)
    if len(df) < initial_len:
        print(f"      Dropped {initial_len - len(df):,} rows with NaN values")

    counts = df["status"].value_counts()
    print(f"\n      Class distribution:")
    print(f"        Legitimate (0): {counts.get(0, 0):>9,}")
    print(f"        Phishing   (1): {counts.get(1, 0):>9,}")
    print(f"        Phish ratio   : {counts.get(1, 0) / max(counts.get(0, 1), 1):.3f}")

    # ── 2. Feature extraction ────────────────────────────────────────
    print(f"\n[2/7] Feature extraction ({len(FEATURE_NAMES)} features per URL)")
    X = extract_features_batch(df["url"])
    y = df["status"].values.astype(int)
    print(f"      Feature matrix shape: {X.shape}")

    # ── 3. Train / test split ────────────────────────────────────────
    print(f"\n[3/7] Train/test split (80/20, stratified) ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"      Train: {len(X_train):,}   Test: {len(X_test):,}")

    # ── 4. Train model ───────────────────────────────────────────────
    print(f"\n[4/7] Training Random Forest (200 trees, all CPU cores) ...")
    t0 = time.time()
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=25,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
        verbose=0,
    )
    model.fit(X_train, y_train)
    train_time = time.time() - t0
    print(f"      Training complete in {train_time:.1f}s")

    # ── 5. Evaluate on test set ──────────────────────────────────────
    print(f"\n[5/7] Evaluating on test set ...")
    print("─" * 65)

    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)
    auc  = roc_auc_score(y_test, y_proba)

    print(f"\n  Accuracy  : {acc:.4f}  ({acc * 100:.2f}%)")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1 Score  : {f1:.4f}")
    print(f"  ROC-AUC   : {auc:.4f}")

    cm = confusion_matrix(y_test, y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"                  Pred Legit  Pred Phish")
    print(f"  Actual Legit  :  {cm[0][0]:>9,}  {cm[0][1]:>9,}")
    print(f"  Actual Phish  :  {cm[1][0]:>9,}  {cm[1][1]:>9,}")

    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["Legitimate", "Phishing"]))

    # ── 6. Feature importances ───────────────────────────────────────
    print("─" * 65)
    print(f"\n[6/7] Top 15 Feature Importances:")
    importances = model.feature_importances_
    ranked = sorted(zip(FEATURE_NAMES, importances), key=lambda x: -x[1])
    for rank, (feat, imp) in enumerate(ranked[:15], 1):
        bar = "#" * int(imp * 100)
        print(f"  {rank:>2}. {feat:<32s}  {imp:.4f}  {bar}")

    # ── 6b. Cross-validation ─────────────────────────────────────────
    print(f"\n  5-fold cross-validation (50k sample) ...")
    sample_size = min(50_000, len(X))
    rng = np.random.RandomState(42)
    idx = rng.choice(len(X), sample_size, replace=False)
    cv_scores = cross_val_score(
        model, X.iloc[idx], y[idx], cv=5, scoring="accuracy", n_jobs=-1
    )
    print(f"  CV Accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    print(f"  Folds: {[f'{s:.4f}' for s in cv_scores]}")

    # ── 7. Save ──────────────────────────────────────────────────────
    print(f"\n[7/7] Saving model ...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    print(f"      Model saved  -> {MODEL_PATH}")

    metadata = {
        "feature_names": FEATURE_NAMES,
        "model_type": "RandomForestClassifier",
        "n_estimators": 200,
        "max_depth": 25,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "roc_auc": auc,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "training_date": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    joblib.dump(metadata, FEATURE_META_PATH)
    print(f"      Metadata saved -> {FEATURE_META_PATH}")

    print(f"\n{'=' * 65}")
    print(f"  TRAINING COMPLETE")
    print(f"  Accuracy: {acc * 100:.2f}%  |  F1: {f1:.4f}  |  AUC: {auc:.4f}")
    print(f"  Model: {MODEL_PATH}")
    print(f"{'=' * 65}\n")

    # ── Quick inference demo ─────────────────────────────────────────
    print("[Demo] Quick inference on sample URLs:")
    demos = [
        ("google.com",                                      "safe"),
        ("facebook.com",                                    "safe"),
        ("github.com",                                      "safe"),
        ("amazon.com",                                      "safe"),
        ("secure-login-paypal.com.suspicious-site.tk",      "phish"),
        ("192.168.1.1/login/verify-account.html",           "phish"),
        ("bit.ly/3xYz123",                                  "short"),
        ("my-bank-secure-login.xyz/account/verify?user=1",  "phish"),
    ]
    for url, expected in demos:
        feats = pd.DataFrame([extract_features(url)], columns=FEATURE_NAMES)
        pred  = model.predict(feats)[0]
        prob  = model.predict_proba(feats)[0][1]
        label = "PHISHING" if pred == 1 else "SAFE    "
        print(f"  [{label}] ({prob:.1%})  {url}")

    print("\n[OK] Model is ready for the PhishGuard backend.\n")


if __name__ == "__main__":
    main()
