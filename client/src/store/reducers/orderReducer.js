import {
    CREATE_ORDER_START,
    CREATE_ORDER_SUCCESS,
    CREATE_ORDER_FAIL,
} from "../actions/orderActions";

const initialState = {
    loading: false,
    orderData: {},
    error: null,
};

const orderReducer = (state = initialState, action) => {
    switch (action.type) {
        case CREATE_ORDER_START:
            return { ...state, loading: true };
        case CREATE_ORDER_SUCCESS:
            return {
                ...state,
                loading: false,
                orderData: action.payload,
                error: null,
            };
        case CREATE_ORDER_FAIL:
            return { ...state, loading: false, error: action.payload };
        default:
            return state;
    }
};

export default orderReducer;
