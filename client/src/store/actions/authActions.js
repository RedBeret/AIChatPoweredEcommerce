//authActions.js
export const authenticateUser =
    (username, password, setLoginError, setLoginSuccess, history) =>
    async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || "Authentication failed");
            }

            const data = await response.json();
            dispatch({
                type: "AUTH_SUCCESS",
                payload: {
                    user: data,
                },
            });
            setLoginSuccess("Login successful");
            // history.push("/");
        } catch (error) {
            console.error("Error during login:", error);
            dispatch({ type: "AUTH_FAIL" });
            setLoginError(error.toString());
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
                    user: data.user,
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
            // setTimeout(() => history.push("/"), 1000);
        } catch (error) {
            console.error("Error during signup:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setSignupError(error.message);
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
        await fetch("/logout", {
            method: "POST",
            credentials: "include",
        });
    } catch (error) {
        console.error("Error during logout:", error);
    } finally {
        dispatch({ type: "AUTH_LOGOUT" });
        history.push("/auth/login");
    }
};
