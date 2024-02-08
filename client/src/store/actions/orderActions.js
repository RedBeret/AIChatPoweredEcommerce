// Order Action Types
export const CREATE_ORDER_START = "CREATE_ORDER_START";
export const CREATE_ORDER_SUCCESS = "CREATE_ORDER_SUCCESS";
export const CREATE_ORDER_FAIL = "CREATE_ORDER_FAIL";

// Action Creators for creating an order
export const createOrderStart = () => ({
    type: CREATE_ORDER_START,
});

export const createOrderSuccess = (orderData) => ({
    type: CREATE_ORDER_SUCCESS,
    payload: orderData,
});

export const createOrderFail = (error) => ({
    type: CREATE_ORDER_FAIL,
    payload: error,
});

export const createOrder = (orderDetails) => async (dispatch) => {
    dispatch(createOrderStart());
    try {
        const response = await fetch("/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(orderDetails),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || "Failed to create order.");
        }

        const data = await response.json();
        dispatch(createOrderSuccess(data));
        return { payload: data };
    } catch (error) {
        dispatch(createOrderFail(error.message));
        return { error: error.message };
    }
};
