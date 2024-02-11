import {
    SEND_MESSAGE_START,
    SEND_MESSAGE_SUCCESS,
    SEND_MESSAGE_FAILURE,
    ADD_USER_MESSAGE,
    ADD_AI_RESPONSE,
} from "../actions/chatActions";

const initialState = {
    messages: [],
    isLoading: false,
    error: null,
};

const chatReducer = (state = initialState, action) => {
    switch (action.type) {
        case SEND_MESSAGE_START:
            return { ...state, isLoading: true, error: null };
        case ADD_USER_MESSAGE:
            const userMessage = {
                id: state.messages.length + 1,
                text: action.payload,
                sender: "user",
            };
            return { ...state, messages: [...state.messages, userMessage] };
        case ADD_AI_RESPONSE:
            const aiResponse = {
                id: state.messages.length + 1,
                text: action.payload,
                sender: "ai",
            };
            return {
                ...state,
                messages: [...state.messages, aiResponse],
                isLoading: false,
            };
        case SEND_MESSAGE_SUCCESS:
            return { ...state, isLoading: false, error: null };
        case SEND_MESSAGE_FAILURE:
            return { ...state, isLoading: false, error: action.payload };
        default:
            return state;
    }
};

export default chatReducer;
