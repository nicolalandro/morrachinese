import streamlit as st
import streamlit.components.v1 as components
import asyncio
from datetime import datetime

MAX_ACTIVE_USERS = 1000

if not hasattr(st, 'static_state'):
    st.static_state = {'games': {}, 'users': {}}

def create_game():
    return {
        'rounds': [[None, None]]
    }
def create_user_status(game_id, user_number, name):
    return {
        'game_id': game_id,
        'user_number': user_number,
        'name': name
    }

async def watch(game_area, game_id, user):
    while True:
        if st.static_state['users'][name]['game_id'] is None:
            st.write('The match end! You win?')
            st.button('Press to restart')
            break
        st.static_state['users'][name]['updated_at'] = datetime.now()
        game_status = []

        for i, round in enumerate(st.static_state['games'][game_id]['rounds'][:-1]):
           game_status.append(f'{i}: {round}')
        game_status.append('users:' + str(st.static_state['games'][game_id]['users']))
        if None in st.static_state['games'][game_id]['rounds'][-1]:
            game_status.append('one of the player do not play')
        game_status.reverse()
        game_area.markdown('\n\n'.join(game_status))
        r = await asyncio.sleep(1)

if __name__ == '__main__':
    st.title('Sasso Carta Forbici')
    # clear unused user
    # clear unused game
    # set user_id and create user
    if len(st.static_state['users'].keys()) > MAX_ACTIVE_USERS:
        "The server is busy!"
    else:
        name = st.text_input("UserName", "Rand")
        user_id = name
        show_messages = ''
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Create game'):
                game_id = str(user_id)
                st.static_state['games'][game_id] = create_game()
                st.static_state['users'][user_id] = create_user_status(game_id, 0, name)
                st.static_state['games'][game_id]['users'] = [user_id]
                show_messages = "you are in game"
        with col2:
            input_game_id = st.text_input("Game ID", "")
        with col3:
            if st.button('Join'):
                if input_game_id in st.static_state['games'].keys():
                    game_id = input_game_id
                    st.static_state['users'][user_id] = create_user_status(game_id, 1, name)
                    st.static_state['games'][game_id]['users'].append(user_id)
                else:
                    show_messages = "game does not exist"
        st.write(show_messages)

        if user_id in st.static_state['users'].keys():
            if st.static_state['users'][user_id]['game_id'] is not None:
                mossa = st.radio(
                    "Choice",
                    ('Sasso', 'Carta', 'Forbice')
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button('Play'):
                        st.static_state['games'][st.static_state['users'][user_id]['game_id']]['rounds'][-1][st.static_state['users'][user_id]['user_number']] = mossa
                        # new round
                        if None not in st.static_state['games'][st.static_state['users'][user_id]['game_id']]['rounds'][-1]:
                            st.static_state['games'][st.static_state['users'][user_id]['game_id']]['rounds'].append([None, None])
                with col2:
                    if st.button('Stop'):
                        for n in st.static_state['games'][st.static_state['users'][user_id]['game_id']]['users']:
                            st.static_state['users'][n]['game_id'] = None
                game_area = st.empty()
                asyncio.run(watch(game_area, st.static_state['users'][user_id]['game_id'], user_id))
