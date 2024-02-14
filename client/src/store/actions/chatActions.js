export const SEND_MESSAGE_START = "SEND_MESSAGE_START";
export const SEND_MESSAGE_SUCCESS = "SEND_MESSAGE_SUCCESS";
export const SEND_MESSAGE_FAILURE = "SEND_MESSAGE_FAILURE";
export const ADD_USER_MESSAGE = "ADD_USER_MESSAGE";
export const ADD_AI_RESPONSE = "ADD_AI_RESPONSE";
export const CONTINUE_LAST_CHAT_SESSION = "CONTINUE_LAST_CHAT_SESSION";
export const SET_MESSAGES = "SET_MESSAGES";
export const FETCH_MESSAGES_ERROR = "FETCH_MESSAGES_ERROR";
export const FETCH_LAST_SESSION_MESSAGES_START =
    "FETCH_LAST_SESSION_MESSAGES_START";
export const FETCH_LAST_SESSION_MESSAGES_SUCCESS =
    "FETCH_LAST_SESSION_MESSAGES_SUCCESS";
export const FETCH_LAST_SESSION_MESSAGES_FAILURE =
    "FETCH_LAST_SESSION_MESSAGES_FAILURE";

export const sendMessage = (messageContent) => async (dispatch) => {
    dispatch({ type: SEND_MESSAGE_START });
    try {
        dispatch({
            type: ADD_USER_MESSAGE,
            payload: messageContent,
        });

        const response = await fetch("/api/chat_messages", {
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
    dispatch({ type: FETCH_LAST_SESSION_MESSAGES_START });
    // console.log("Fetching messages...");
    try {
        const response = await fetch("/api/continue_last_conversation", {
            method: "GET",
            credentials: "include",
        });
        // console.log("Response received:", response);
        if (!response.ok) {
            throw new Error("Failed to fetch messages");
        }
        const data = await response.json();
        // console.log("Data received:", data);

        const messages = data.messages.map((msg, index) => ({
            id: index,
            sender: msg.sender,
            text: msg.text,
        }));
        // console.log("Messages extracted:", messages);

        dispatch({
            type: SET_MESSAGES,
            payload: messages,
        });
        // console.log("Messages dispatched to store");
        // console.log("Current chat messages on Tech:", messages);
    } catch (error) {
        console.error("Fetch error:", error);
        dispatch({
            type: FETCH_LAST_SESSION_MESSAGES_FAILURE,
            payload: error.toString(),
        });
    }
};

export const continueLastChatSession = () => async (dispatch) => {
    dispatch(fetchMessages());
};
