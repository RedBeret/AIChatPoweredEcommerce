import {
    SEND_MESSAGE_START,
    SEND_MESSAGE_SUCCESS,
    SEND_MESSAGE_FAILURE,
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
        case SEND_MESSAGE_SUCCESS:
            return {
                ...state,
                isLoading: false,
                messages: [...state.messages, action.payload],
                error: null,
            };
        case SEND_MESSAGE_FAILURE:
            return { ...state, isLoading: false, error: action.payload };
        default:
            return state;
    }
};

export default chatReducer;
