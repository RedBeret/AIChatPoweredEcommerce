export const SEND_MESSAGE_START = "SEND_MESSAGE_START";
export const SEND_MESSAGE_SUCCESS = "SEND_MESSAGE_SUCCESS";
export const SEND_MESSAGE_FAILURE = "SEND_MESSAGE_FAILURE";
export const ADD_USER_MESSAGE = "ADD_USER_MESSAGE";
export const ADD_AI_RESPONSE = "ADD_AI_RESPONSE";

export const sendMessage = (messageContent) => async (dispatch) => {
    dispatch({ type: SEND_MESSAGE_START });
    try {
        dispatch({
            type: ADD_USER_MESSAGE,
            payload: messageContent,
        });

        const response = await fetch("/chat_messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({ message: messageContent }),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            const errorMessage =
                errorResponse.error || "Failed to get AI response.";
            throw new Error(errorMessage);
        }

        const data = await response.json();

        dispatch({
            type: ADD_AI_RESPONSE,
            payload: data.response,
        });

        dispatch({ type: SEND_MESSAGE_SUCCESS });
    } catch (error) {
        dispatch({
            type: SEND_MESSAGE_FAILURE,
            payload: error.message || "An unexpected error occurred.",
        });
        console.error("Error sending message:", error.message);
    }
};

export const fetchMessages = () => async (dispatch) => {
    try {
        const response = await fetch("/chat_messages", {
            credentials: "include",
        });
        if (response.ok) {
            const data = await response.json();
            dispatch({ type: "SET_MESSAGES", payload: data });
        } else {
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
    }
};
