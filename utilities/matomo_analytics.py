"""Matomo Analytics integration for the Barracks Lawyer application."""
import os
from typing import Optional


def get_matomo_tracking_code() -> str:
    """
    Generate the Matomo tracking code for the application based on environment variables.
    
    Returns:
        str: The HTML tracking code to be included in the page.
    """
    # Get values from environment
    matomo_enabled = os.getenv("MATOMO_ENABLED", "False").lower() == "true"
    matomo_url = os.getenv("MATOMO_URL", "")
    site_id = os.getenv("MATOMO_SITE_ID", "")
    
    if not matomo_enabled or not site_id or not matomo_url:
        return ""  # Return empty string if Matomo is not configured
    
    # Remove trailing slash from URL if present
    if matomo_url.endswith("/"):
        matomo_url = matomo_url[:-1]
    
    # Generate the Matomo tracking code
    tracking_code = f"""
    <!-- Matomo -->
    <script>
      var _paq = window._paq = window._paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {{
        var u="//{matomo_url}/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '{site_id}']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      }})();
    </script>
    <!-- End Matomo Code -->
    """
    
    return tracking_code 