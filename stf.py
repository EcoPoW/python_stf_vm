
def chain_stf(state, data):
    subchains = state.get('subchains', {})
    subchains.update(data.get('subchains', {}))
    new_state = {}
    new_state['subchains'] = subchains
    return new_state
