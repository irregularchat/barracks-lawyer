"""Matomo Analytics integration for the Barracks Lawyer application."""
import os
from typing import Optional


def get_matomo_tracking_code(site_id: Optional[str] = None, matomo_url: Optional[str] = None) -> str:
    """
    Generate the Matomo tracking code for the application.
    
    Args:
        site_id: The Matomo site ID. If None, will try to get from environment.
        matomo_url: The Matomo server URL. If None, will try to get from environment.
        
    Returns:
        str: The HTML tracking code to be included in the page.
    """
    # Get values from environment if not provided
    site_id = site_id or os.getenv("MATOMO_SITE_ID")
    matomo_url = matomo_url or os.getenv("MATOMO_URL")
    
    # Check if Matomo is enabled
    matomo_enabled = os.getenv("MATOMO_ENABLED", "False").lower() == "true"
    
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
        var u="{matomo_url}/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '{site_id}']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      }})();
    </script>
    <!-- End Matomo Code -->
    """
    
    return tracking_code 