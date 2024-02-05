export const authenticateUser =
    (username, password, setError, history) => async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Authentication failed");
            }

            dispatch({
                type: "AUTH_SUCCESS",
                payload: { accessToken: data.access_token, user: username },
            });

            setTimeout(() => history.push("/"), 1000);
        } catch (error) {
            console.error("Error during login:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.message);
        }
    };

export const checkLoginSession = () => async (dispatch) => {
    try {
        const response = await fetch("/check_session", {
            method: "GET",
            credentials: "include",
        });
        const data = await response.json();
        if (!response.ok) throw new Error("Session check failed");

        dispatch({
            type: "AUTH_SUCCESS",
            payload: {
                accessToken: data.accessToken,
                user: {
                    id: data.id,
                    username: data.username,
                    email: data.email,
                },
            },
        });
    } catch (error) {
        console.error("Session check error:", error);
        dispatch({ type: "AUTH_LOGOUT" });
    }
};

export const registerUser =
    (userData, setSignupError, setSignupSuccess, history) =>
    async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/user_auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Signup failed");
            }

            dispatch({ type: "AUTH_SUCCESS", payload: { user: data.user } });
            setSignupSuccess("Signup successful!");
            setTimeout(() => history.push("/"), 1000);
        } catch (error) {
            console.error("Error during signup:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setSignupError(error.message);
        }
    };

export const updatePassword =
    (username, oldPassword, newPassword, setError, setSuccess, history) =>
    async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/user_auth", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    username,
                    password: oldPassword,
                    newPassword,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Password update failed");
            }

            dispatch({ type: "UPDATE_PASSWORD_SUCCESS" });
            setSuccess("Password updated successfully!");
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
            setTimeout(() => history.push("/signup"), 1000);
        } catch (error) {
            console.error("Error during account deletion:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.message);
        }
    };
