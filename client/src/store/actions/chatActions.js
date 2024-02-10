export const SEND_MESSAGE_START = "SEND_MESSAGE_START";
export const SEND_MESSAGE_SUCCESS = "SEND_MESSAGE_SUCCESS";
export const SEND_MESSAGE_FAILURE = "SEND_MESSAGE_FAILURE";

// This action creator sends the message to the backend, which now uses OpenAI's assistant
export const sendMessage = (messageContent) => async (dispatch) => {
    dispatch({ type: SEND_MESSAGE_START });
    try {
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
            throw new Error(
                errorResponse.error || "Network response was not ok"
            );
        }

        const data = await response.json();

        dispatch({
            type: SEND_MESSAGE_SUCCESS,
            payload: {
                userMessage: messageContent,
                aiResponse: data.ai_response,
            },
        });
    } catch (error) {
        dispatch({
            type: SEND_MESSAGE_FAILURE,
            payload: error.toString(),
        });
        console.error("Error sending message:", error);
    }
};
