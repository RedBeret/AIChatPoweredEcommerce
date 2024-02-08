import {
    CREATE_SHIPPING_INFO_START,
    CREATE_SHIPPING_INFO_SUCCESS,
    CREATE_SHIPPING_INFO_FAIL,
} from "../actions/shippingActions";

const initialState = {
    loading: false,
    shippingInfo: {},
    error: null,
};

const shippingReducer = (state = initialState, action) => {
    switch (action.type) {
        case CREATE_SHIPPING_INFO_START:
            return { ...state, loading: true };
        case CREATE_SHIPPING_INFO_SUCCESS:
            return {
                ...state,
                loading: false,
                shippingInfo: action.payload,
                error: null,
            };
        case CREATE_SHIPPING_INFO_FAIL:
            return { ...state, loading: false, error: action.payload };
        default:
            return state;
    }
};

export default shippingReducer;
