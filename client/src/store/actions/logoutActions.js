// logoutActions.js
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
        history.push("/login");
    }
};
