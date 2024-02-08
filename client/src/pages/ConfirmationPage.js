import React from "react";
import { useLocation } from "react-router-dom";

const Confirmation = () => {
    const location = useLocation();
    const { confirmationNumber } = location.state || {};

    return (
        <div>
            <h1>Order Confirmation</h1>
            {confirmationNumber ? (
                <p>
                    Your order has been confirmed. Confirmation number:{" "}
                    {confirmationNumber}
                </p>
            ) : (
                <p>Order confirmation number is not available.</p>
            )}
        </div>
    );
};

export default Confirmation;
