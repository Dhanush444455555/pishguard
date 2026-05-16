"""
PhishGuard AI — Threat Explainer Service
=========================================
Provides human-readable explanations for why a URL was flagged as
phishing based on the extracted features.
"""

from typing import List


class ThreatExplainer:
    """
    Analyzes feature values and generates natural language explanations.
    """

    def explain(self, features: dict) -> List[str]:
        """
        Analyze features and return a list of threat indicators.
        """
        explanations = []

        # 1. Domain/Hostname checks
        if features.get("has_ip_address"):
            explanations.append("The URL uses a raw IP address instead of a domain name, which is a common phishing tactic.")
        
        if features.get("is_shortened"):
            explanations.append("The URL uses a known link shortening service, often used to hide the final destination.")
        
        if features.get("has_suspicious_tld"):
            explanations.append("The URL uses a top-level domain (TLD) frequently associated with malicious activity.")

        if features.get("num_subdomains", 0) > 2:
            explanations.append(f"The URL contains an unusually high number of subdomains ({features['num_subdomains']}).")

        # 2. Structural checks
        if features.get("url_length", 0) > 100:
            explanations.append("The URL is exceptionally long, which may be used to obscure the true domain.")
        
        if features.get("num_dots", 0) > 4:
            explanations.append("The URL contains a high number of dots, often used to mimic legitimate domains.")

        if features.get("has_at_symbol"):
            explanations.append("The URL contains an '@' symbol, which can be used to ignore everything before it and redirect the user.")

        if features.get("has_double_slash_redirect"):
            explanations.append("The URL contains a double slash ('//') in the path, which can trigger redirects to malicious sites.")

        # 3. Content/Keyword checks
        if features.get("has_suspicious_keyword"):
            explanations.append("The URL contains keywords typical of phishing scams (e.g., 'login', 'verify', 'account').")

        if not features.get("has_https"):
            explanations.append("The connection is not secured with HTTPS, making it easier for attackers to intercept data.")

        # 4. Complexity checks
        if features.get("url_entropy", 0) > 4.5:
            explanations.append("The URL string has high complexity/randomness, typical of auto-generated malicious links.")

        if not explanations:
            explanations.append("The URL exhibits subtle patterns common in phishing attacks, though no single major red flag was found.")

        return explanations


_explainer = ThreatExplainer()

def get_explainer() -> ThreatExplainer:
    return _explainer
