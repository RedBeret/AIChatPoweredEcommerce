import {
    SEND_MESSAGE_START,
    SEND_MESSAGE_SUCCESS,
    SEND_MESSAGE_FAILURE,
    ADD_USER_MESSAGE,
    ADD_AI_RESPONSE,
    // START_NEW_CHAT_SESSION,
    SET_MESSAGES,
    FETCH_LAST_SESSION_MESSAGES_START,
    FETCH_LAST_SESSION_MESSAGES_SUCCESS,
    FETCH_LAST_SESSION_MESSAGES_FAILURE,
} from "../actions/chatActions";

// Your reducer logic...

const initialState = {
    messages: [],
    isLoading: false,
    error: null,
};

const chatReducer = (state = initialState, action) => {
    switch (action.type) {
        case SEND_MESSAGE_START:
            return { ...state, isLoading: true, error: null };
        case SEND_MESSAGE_SUCCESS:
            return { ...state, isLoading: false, error: null };
        case SEND_MESSAGE_FAILURE:
            return { ...state, isLoading: false, error: action.payload };
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

        // case START_NEW_CHAT_SESSION:
        //     return { ...initialState };
        case SET_MESSAGES:
            return {
                ...state,
                messages: action.payload || [],
                isLoading: false,
            };

        case FETCH_LAST_SESSION_MESSAGES_START:
            return { ...state, isLoading: true, error: null };
        case FETCH_LAST_SESSION_MESSAGES_SUCCESS:
            return { ...state, messages: action.payload, isLoading: false };
        case FETCH_LAST_SESSION_MESSAGES_FAILURE:
            return { ...state, isLoading: false, error: action.payload };
        case "CLEAR_CHAT_MESSAGES":
            return { ...state, messages: [] };
        default:
            return state;
    }
};

export default chatReducer;
