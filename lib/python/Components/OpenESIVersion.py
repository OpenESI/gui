"""
OpenESI Version Information
File di identificazione ufficiale OpenESI 10
"""

class OpenESIVersion:
    """Informazioni versione OpenESI"""
    
    MAJOR = 10
    MINOR = 0
    REVISION = 0
    BUILD = 1
    
    CODENAME = "Phoenix"
    EDITION = "Community"
    
    @classmethod
    def getVersionString(cls):
        """Restituisce stringa versione completa"""
        return f"OpenESI {cls.MAJOR}.{cls.MINOR}.{cls.REVISION} {cls.CODENAME}"
    
    @classmethod
    def getBuildString(cls):
        """Restituisce stringa build"""
        return f"Build {cls.BUILD}"
    
    @classmethod
    def getFullVersion(cls):
        """Restituisce informazioni versione complete"""
        return {
            'name': 'OpenESI',
            'version': f"{cls.MAJOR}.{cls.MINOR}.{cls.REVISION}",
            'build': cls.BUILD,
            'codename': cls.CODENAME,
            'edition': cls.EDITION
        }

# Istanze globali per compatibilità
version = OpenESIVersion()
