const messagesInitialState = {
    messages: [],
};

const messagesReducer = (state = messagesInitialState, action) => {
    switch (action.type) {
        case "CLEAR_USER_DATA":
            return messagesInitialState;
        default:
            return state;
    }
};

export default messagesReducer;
