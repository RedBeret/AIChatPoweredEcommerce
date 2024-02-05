import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { useCartContext } from "../components/CartContext";

const CheckoutSchema = Yup.object().shape({
    email: Yup.string().email("Invalid email").required("Required"),
    firstName: Yup.string().required("Required"),
    lastName: Yup.string().required("Required"),
    address: Yup.string().required("Required"),
    city: Yup.string().required("Required"),
    state: Yup.string().required("Required"),
    zip: Yup.string().required("Required"),
});

const Checkout = () => {
    const { cartItems } = useCartContext();

    const calculateTotal = () => {
        return cartItems
            .reduce((total, item) => total + item.price * item.quantity, 0)
            .toFixed(2);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Checkout</h1>

            {/* Cart Items */}
            <div className="mb-6">
                {cartItems.map((item) => (
                    <div
                        key={item.id}
                        className="flex justify-between items-center bg-white p-4 rounded-md mb-2 shadow"
                    >
                        <div className="flex items-center">
                            <img
                                className="w-16 h-16 object-cover rounded mr-4"
                                src={`/assets/${item.image_url}`}
                                alt={item.name}
                            />
                            <div>
                                <h5 className="font-bold">{item.name}</h5>
                                <p className="text-sm text-gray-500">
                                    Quantity: {item.quantity}
                                </p>
                            </div>
                        </div>
                        <span className="font-semibold">
                            ${(item.price * item.quantity).toFixed(2)}
                        </span>
                    </div>
                ))}
                <p className="text-xl font-bold">Total: ${calculateTotal()}</p>
            </div>

            {/* Checkout Form */}
            <Formik
                initialValues={{
                    email: "",
                    firstName: "",
                    lastName: "",
                    address: "",
                    city: "",
                    state: "",
                    zip: "",
                    cardName: "",
                    cardNumber: "",
                    expDate: "",
                    cvv: "",
                }}
                validationSchema={CheckoutSchema}
                onSubmit={async (values, actions) => {
                    try {
                        const orderDetails = cartItems.map((item) => ({
                            product_id: item.id,
                            quantity: item.quantity,
                        }));

                        const response = await fetch("/api/orders", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                // user_id: ,
                                order_details: orderDetails,
                            }),
                        });

                        if (!response.ok) {
                            throw new Error("Network response was not ok.");
                        }
                        console.log("Order placed successfully!");
                        actions.resetForm();
                        window.location.href = "/order-confirmation";
                    } catch (error) {
                        console.error(
                            "There was a problem with your fetch operation:",
                            error
                        );
                    }

                    actions.setSubmitting(false);
                }}
            >
                {({ isSubmitting }) => (
                    <Form className="bg-white p-4 rounded-md shadow">
                        {/* Form fields */}
                        <div className="grid gap-4 sm:grid-cols-2 mb-4">
                            <Field
                                name="firstName"
                                placeholder="First Name"
                                className="p-2 border rounded"
                            />
                            <Field
                                name="lastName"
                                placeholder="Last Name"
                                className="p-2 border rounded"
                            />
                        </div>
                        <Field
                            name="email"
                            type="email"
                            placeholder="Email"
                            className="p-2 border rounded w-full mb-4"
                        />
                        <Field
                            name="address"
                            placeholder="Address"
                            className="p-2 border rounded w-full mb-4"
                        />
                        <div className="grid gap-4 sm:grid-cols-3 mb-4">
                            <Field
                                name="city"
                                placeholder="City"
                                className="p-2 border rounded"
                            />
                            <Field
                                name="state"
                                placeholder="State"
                                className="p-2 border rounded"
                            />
                            <Field
                                name="zip"
                                placeholder="ZIP / Postal Code"
                                className="p-2 border rounded"
                            />
                        </div>

                        {/* Payment Information */}
                        <h2 className="text-xl font-bold mb-4">
                            Payment Information
                        </h2>
                        <div className="w-full p-3">
                            <label
                                htmlFor="type2"
                                className="flex items-center cursor-pointer"
                            >
                                <input
                                    type="radio"
                                    className="form-radio h-5 w-5 text-indigo-500"
                                    name="type"
                                    id="type2"
                                />
                                <img
                                    src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg"
                                    width="80"
                                    className="ml-3"
                                    alt="PayPal"
                                />
                            </label>
                        </div>

                        {/* Submit button */}
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                        >
                            Pay Now
                        </button>
                    </Form>
                )}
            </Formik>
        </div>
    );
};

export default Checkout;
