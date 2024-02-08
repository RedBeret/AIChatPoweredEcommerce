import React from "react";
import { useLocation } from "react-router-dom";
import logo from "../assets/img/vision_x_logo.png";

const Confirmation = () => {
    const location = useLocation();
    const { confirmationNumber } = location.state || {};

    return (
        <div
            className="flex justify-center items-center bg-gray-100 p-4"
            style={{ height: "75vh" }}
        >
            <div className="w-full max-w-lg my-8">
                <div className="bg-white shadow-xl rounded-lg py-3">
                    <div className="photo-wrapper p-2">
                        <img
                            className="w-32 h-32 rounded-full mx-auto"
                            src={logo}
                            alt="Logo"
                        />
                    </div>
                    <div className="p-4">
                        <h1 className="text-center text-xl font-bold text-gray-900">
                            Payment successful
                        </h1>
                        <h2 className="text-center text-3xl font-bold text-gray-900 my-4">
                            Thanks for ordering
                        </h2>
                        <p className="text-center text-gray-600 mb-4">
                            We appreciate your order, we're currently processing
                            it. So hang tight and we'll send you confirmation
                            very soon!
                        </p>
                    </div>
                    <div className="p-4 bg-gray-100 rounded-b-lg">
                        {confirmationNumber ? (
                            <div className="flex flex-col items-center">
                                <h3 className="text-lg font-bold text-gray-900">
                                    Order Confirmation
                                </h3>
                                <p className="text-gray-600">
                                    Your order has been confirmed.
                                </p>
                                <p className="text-gray-600">
                                    Confirmation number:{" "}
                                    <span className="text-gray-900 font-bold">
                                        {confirmationNumber}
                                    </span>
                                </p>
                            </div>
                        ) : (
                            <p className="text-red-500 text-center">
                                Order confirmation number is not available.
                            </p>
                        )}
                    </div>
                    <div className="p-4">
                        <h1 className="text-center text-l font-bold text-gray-900">
                            Free Premium Technical Support Added
                        </h1>

                        <p className="text-center text-gray-600 mb-4">
                            While logged in you will now see a new menu option
                            for technical support for any needs you may have.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Confirmation;
