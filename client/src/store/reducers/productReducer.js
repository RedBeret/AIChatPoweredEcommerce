const initialState = {
    productList: [],
    selectedProduct: null,
    isLoading: false,
    error: null,
};

const productReducer = (state = initialState, action) => {
    switch (action.type) {
        case "FETCH_PRODUCTS_START":
        case "FETCH_PRODUCT_START":
            return { ...state, isLoading: true, error: null };
        case "FETCH_PRODUCTS_SUCCESS":
            return {
                ...state,
                isLoading: false,
                productList: action.payload,
                error: null,
            };
        case "FETCH_PRODUCT_SUCCESS":
            return {
                ...state,
                isLoading: false,
                selectedProduct: action.payload,
                error: null,
            };
        case "FETCH_PRODUCTS_FAILURE":
        case "FETCH_PRODUCT_FAILURE":
            return { ...state, isLoading: false, error: action.payload };
        default:
            return state;
    }
};

export default productReducer;
