// src/store/orders/orderActions.js

// Action Types
export const CREATE_ORDER_START = "CREATE_ORDER_START";
export const CREATE_ORDER_SUCCESS = "CREATE_ORDER_SUCCESS";
export const CREATE_ORDER_FAIL = "CREATE_ORDER_FAIL";

// Action Creators

// Signals the start of creating an order
export const createOrderStart = () => ({
    type: CREATE_ORDER_START,
});

// Handles the success of order creation
export const createOrderSuccess = (orderData) => ({
    type: CREATE_ORDER_SUCCESS,
    payload: orderData,
});

// Handles the failure of order creation
export const createOrderFail = (error) => ({
    type: CREATE_ORDER_FAIL,
    payload: error,
});

// Performs the order creation operation
export const createOrder = (orderDetails) => async (dispatch) => {
    dispatch(createOrderStart());
    try {
        // Attempt to create an order through your API
        const response = await fetch("/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(orderDetails),
        });

        // Handle non-OK responses
        if (!response.ok) throw new Error("Order creation failed");

        // Dispatch success action with order data
        const data = await response.json();
        dispatch(createOrderSuccess(data));
    } catch (error) {
        // Dispatch failure action with error message
        dispatch(createOrderFail(error.message));
    }
};
