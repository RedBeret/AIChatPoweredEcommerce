// Action Types
export const FETCH_PRODUCTS_START = "FETCH_PRODUCTS_START";
export const FETCH_PRODUCTS_SUCCESS = "FETCH_PRODUCTS_SUCCESS";
export const FETCH_PRODUCTS_FAILURE = "FETCH_PRODUCTS_FAILURE";

export const FETCH_PRODUCT_START = "FETCH_PRODUCT_START";
export const FETCH_PRODUCT_SUCCESS = "FETCH_PRODUCT_SUCCESS";
export const FETCH_PRODUCT_FAILURE = "FETCH_PRODUCT_FAILURE";

// Fetch all products
export const fetchProductsStart = () => ({
    type: FETCH_PRODUCTS_START,
});

export const fetchProductsSuccess = (products) => ({
    type: FETCH_PRODUCTS_SUCCESS,
    payload: products,
});

export const fetchProductsFailure = (error) => ({
    type: FETCH_PRODUCTS_FAILURE,
    payload: error,
});

export const fetchProducts = () => async (dispatch) => {
    dispatch(fetchProductsStart());
    try {
        const response = await fetch("/api/product");
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        dispatch(fetchProductsSuccess(data));
    } catch (error) {
        dispatch(fetchProductsFailure(error.toString()));
    }
};

export const fetchProductStart = () => ({
    type: FETCH_PRODUCT_START,
});

export const fetchProductSuccess = (product) => ({
    type: FETCH_PRODUCT_SUCCESS,
    payload: product,
});

export const fetchProductFailure = (error) => ({
    type: FETCH_PRODUCT_FAILURE,
    payload: error,
});

export const fetchProduct = (productId) => async (dispatch) => {
    dispatch(fetchProductStart());
    try {
        const response = await fetch(`/api/product/${productId}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const product = await response.json();
        dispatch(fetchProductSuccess(product));
    } catch (error) {
        dispatch(fetchProductFailure(error.toString()));
    }
};
