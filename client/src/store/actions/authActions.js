export const authenticateUser =
    (username, password, setError, history) => async (dispatch) => {
        dispatch({ type: "AUTH_START" });
        try {
            const response = await fetch("http://localhost:5555/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (!response.ok)
                throw new Error(data.error || "Authentication failed");

            dispatch({
                type: "AUTH_SUCCESS",
                payload: { accessToken: data.access_token, user: username },
            });

            history.push("/"); // Redirect to home page on successful login
        } catch (error) {
            console.error("Error during login:", error);
            dispatch({ type: "AUTH_FAIL", payload: error.message });
            setError(error.message); // Set login error state in the component
        }
    };
