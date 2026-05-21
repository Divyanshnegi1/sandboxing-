def get_network_mode(restricted=False):
    # If restricted, disable network by setting to 'none'
    return "none" if restricted else "bridge"

