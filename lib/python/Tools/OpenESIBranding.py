"""
OpenESI Branding Information
Configurazione branding e identificazione
"""

class OpenESIBranding:
    """Configurazione branding OpenESI"""
    
    # Informazioni progetto
    PROJECT_NAME = "OpenESI"
    PROJECT_VERSION = "10.0"
    PROJECT_URL = "https://github.com/OpenESI"
    PROJECT_DESCRIPTION = "Open Embedded System Interface"
    
    # Informazioni copyright
    COPYRIGHT = "© OpenESI Project"
    LICENSE = "GPL-2.0"
    DEVELOPERS = "OpenESI Development Team"
    
    # Configurazioni branding
    BOOTLOGO_NAME = "opensesi"
    SPLASH_NAME = "opensesi"
    SKIN_PREFIX = "opensesi"
    
    @classmethod
    def getBoxBrand(cls):
        """Restituisce nome branding box"""
        return cls.PROJECT_NAME
    
    @classmethod
    def getImageVersion(cls):
        """Restituisce versione immagine"""
        return cls.PROJECT_VERSION
    
    @classmethod
    def getProjectURL(cls):
        """Restituisce URL progetto"""
        return cls.PROJECT_URL
    
    @classmethod 
    def getBrandingInfo(cls):
        """Restituisce tutte le info branding"""
        return {
            'name': cls.PROJECT_NAME,
            'version': cls.PROJECT_VERSION,
            'url': cls.PROJECT_URL,
            'description': cls.PROJECT_DESCRIPTION,
            'copyright': cls.COPYRIGHT,
            'license': cls.LICENSE,
            'developers': cls.DEVELOPERS
        }

# Istanza globale
branding = OpenESIBranding()
