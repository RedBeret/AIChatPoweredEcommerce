//authReducer.js
const initialState = {
    accessToken: null,
    isAuthenticated: false,
    user: null,
    loading: false,
    error: null,
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case "AUTH_START":
            return { ...state, loading: true, error: null };
        case "AUTH_SUCCESS":
            return {
                ...state,
                accessToken: action.payload.accessToken,
                isAuthenticated: true,
                loading: false,
                user: action.payload.user,
            };
        case "AUTH_FAIL":
            return { ...state, loading: false, error: action.payload };
        case "AUTH_LOGOUT":
            return {
                ...state,
                accessToken: null,
                isAuthenticated: false,
                user: null,
            };
        default:
            return state;
    }
};

export default authReducer;
