// Shipping Action Types
export const CREATE_SHIPPING_INFO_START = "CREATE_SHIPPING_INFO_START";
export const CREATE_SHIPPING_INFO_SUCCESS = "CREATE_SHIPPING_INFO_SUCCESS";
export const CREATE_SHIPPING_INFO_FAIL = "CREATE_SHIPPING_INFO_FAIL";

// Action Creators for Shipping Info

export const createShippingInfoStart = () => ({
    type: CREATE_SHIPPING_INFO_START,
});

export const createShippingInfoSuccess = (shippingInfo) => ({
    type: CREATE_SHIPPING_INFO_SUCCESS,
    payload: shippingInfo,
});

export const createShippingInfoFail = (error) => ({
    type: CREATE_SHIPPING_INFO_FAIL,
    payload: error,
});

export const createShippingInfo = (shippingData) => async (dispatch) => {
    dispatch(createShippingInfoStart());
    try {
        const response = await fetch("/shipping_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(shippingData),
        });

        const data = await response.json();

        if (!response.ok) {
            // Assuming that the server's response will contain an 'error' field in the JSON body if there is an error
            dispatch(
                createShippingInfoFail(
                    data.error || "Failed to create shipping information."
                )
            );
            return {
                error: data.error || "Failed to create shipping information.",
            }; // Return an object containing the error
        }

        console.log("Shipping info created:", data);
        dispatch(createShippingInfoSuccess(data));
        return { payload: data }; // Return an object containing the payload
    } catch (error) {
        console.error("Error creating shipping info:", error);
        dispatch(createShippingInfoFail(error.toString()));
        return { error: error.toString() }; // Return an object containing the error
    }
};
