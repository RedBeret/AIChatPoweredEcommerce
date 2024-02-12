const messagesInitialState = {
    messages: [],
};

const messagesReducer = (state = messagesInitialState, action) => {
    switch (action.type) {
        case "CLEAR_USER_DATA":
            return messagesInitialState;
        case "SET_MESSAGES":
            return {
                ...state,
                messages: action.payload,
            };
        default:
            return state;
    }
};

export default messagesReducer;
