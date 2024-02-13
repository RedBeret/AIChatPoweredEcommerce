// import { fetchMessages } from "./chatActions";
//authActions.js
export const authenticateUser =
    (username, password, setError, setSuccess, history) =>
    async (dispatch, getState) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw errorData.message || "Authentication failed";
            }
            const data = await response.json();

            dispatch({
                type: "AUTH_SUCCESS",
                payload: {
                    user: data,
                },
            });

            setSuccess("Login successful");
            const { chat } = getState();
            console.log("Current chat messages:", chat.messages);
            if (chat.messages.length === 0) {
                console.log("Fetching messages...");
                // dispatch(fetchMessages());
            } else {
                console.log("Chat messages already fetched.");
            }
        } catch (error) {
            console.error("Error during login:", error);
            dispatch({ type: "AUTH_FAIL" });
            setError(error.toString());
        }
    };

export const checkLoginSession = () => async (dispatch) => {
    try {
        const response = await fetch("/check_session", {
            method: "GET",
            credentials: "include",
        });

        if (!response.ok) {
            console.error("Session check failed");
            dispatch({ type: "AUTH_LOGOUT" });
            return;
        }

        const data = await response.json();
        if (data && data.user) {
            dispatch({
                type: "AUTH_SUCCESS",
                payload: {
                    user: data,
                },
            });
        } else {
            console.error("User data not found in session check response");
            dispatch({ type: "AUTH_LOGOUT" });
        }
    } catch (error) {
        console.error("Session check error:", error);
        dispatch({ type: "AUTH_LOGOUT" });
    }
};

export const registerUser =
    (userData, setError, setSuccess, history) => async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/user_auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });
            const data = await response.json();
            console.log("Register User Response Data:", data);
            if (!response.ok) {
                throw new Error(data.error || "Signup failed");
            }

            dispatch({ type: "AUTH_SUCCESS", payload: data });
            setSuccess("Signup successful!");
            return { payload: { user: data.user } };
            // setTimeout(() => history.push("/"), 1000);
        } catch (error) {
            console.error("Error during signup:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.toString());
            return { error: { message: error.message } };
        }
    };

export const updatePassword =
    (username, currentPassword, newPassword, setError, setSuccess, history) =>
    async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/user_auth", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    username,
                    password: currentPassword,
                    newPassword,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Password update failed");
            }

            dispatch({ type: "UPDATE_PASSWORD_SUCCESS" });
            setSuccess("Password updated successfully!");
            setTimeout(() => history.push("/auth/login"), 2000);
        } catch (error) {
            console.error("Error during password update:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.message);
        }
    };

export const deleteUser =
    (username, password, setError, setSuccess, history) => async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/user_auth", {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Account deletion failed");
            }

            dispatch({ type: "AUTH_LOGOUT" });
            setSuccess("Account deleted successfully!");
            setTimeout(() => {
                history.push("/auth/login");
            }, 2000);
        } catch (error) {
            console.error("Error during account deletion:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.message);
        }
    };

export const logoutUser = (history) => async (dispatch) => {
    dispatch({ type: "AUTH_START" });
    try {
        const response = await fetch("/logout", {
            method: "POST",
            credentials: "include",
        });
        if (response.ok) {
            dispatch({ type: "AUTH_LOGOUT" });
            dispatch({ type: "CLEAR_USER_DATA" });
            dispatch({ type: "CLEAR_CHAT_MESSAGES" });
            localStorage.removeItem("token");
            history.push("/auth/login");
        } else {
            console.error("Logout failed:", response.statusText);
        }
    } catch (error) {
        console.error("Error during logout:", error);
    }
};
