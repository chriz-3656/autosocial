import os
import glob
import logging

logger = logging.getLogger(__name__)

class CleanupService:
    def __init__(self, tmp_dir: str = "/tmp"):
        self.tmp_dir = tmp_dir
        
    def clean(self):
        """Remove temporary files like generated images"""
        pattern = os.path.join(self.tmp_dir, "*.png")
        files = glob.glob(pattern)
        for f in files:
            try:
                os.remove(f)
                logger.info(f"Removed temp file {f}")
            except Exception as e:
                logger.error(f"Failed to remove {f}: {e}")
