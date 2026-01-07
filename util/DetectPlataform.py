def plataform_detect():
    """
    Detects the current operating system name.
    
    Returns:
        sistema (str): Name of the operating system, e.g. 'Windows', 'Linux', or 'Darwin'.
    """
    import platform
    sistema = platform.system()
    return sistema