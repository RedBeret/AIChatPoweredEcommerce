import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { useCartContext } from "../components/CartContext";
import { registerUser } from "../store/actions/authActions";
import { v4 as uuidv4 } from "uuid";

const Checkout = () => {
    const { cartItems } = useCartContext();
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
    const user = useSelector((state) => state.auth.user);
    const dispatch = useDispatch();
    const history = useHistory();
    const [error, setError] = useState("");
    const [signupError, setSignupError] = useState("");

    const CheckoutSchema = Yup.object().shape({
        firstName: Yup.string().required("First name is required"),
        lastName: Yup.string().required("Last name is required"),
        addressLine1: Yup.string().required("Address Line 1 is required"),
        addressLine2: Yup.string(),
        city: Yup.string().required("City is required"),
        state: Yup.string().required("State is required"),
        zip: Yup.string().required("ZIP code is required"),
        country: Yup.string().required("Country is required"),
        phoneNumber: Yup.string().required("Phone number is required"),
        email: !isAuthenticated
            ? Yup.string().required("Email is required")
            : Yup.string(),
        username: !isAuthenticated
            ? Yup.string().required("Username is required")
            : Yup.string(),
        password: !isAuthenticated
            ? Yup.string().required("Password is required")
            : Yup.string(),
    });

    const calculateTotal = () => {
        return cartItems
            .reduce((total, item) => total + item.price * item.quantity, 0)
            .toFixed(2);
    };
    // const handleUserAuthentication = async (values) => {
    //     try {
    //         await dispatch(authenticateUser(values.username, values.password));
    //         console.log("User authenticated successfully");
    //     } catch (error) {
    //         console.log(
    //             "Authentication failed, attempting registration",
    //             error
    //         );
    //         await dispatch(
    //             registerUser({
    //                 username: values.username,
    //                 password: values.password,
    //                 email: values.email,
    //             })
    //         );
    //         console.log("User registered and authenticated successfully");
    //     }
    // };
    const handleFormSubmit = async (values, actions) => {
        console.log("Form submission started", values);
        let currentUser = user;
        setError("");
        console.log("Authenticating...");

        if (!isAuthenticated) {
            try {
                await dispatch(
                    registerUser(
                        {
                            username: values.username,
                            password: values.password,
                            email: values.email,
                        },
                        setSignupError, // Pass the setSignupError function here
                        () => console.log("Signup successful!"), // Directly passing a success message function for demonstration
                        history
                    )
                );
                console.log("Registration successful");
            } catch (registrationError) {
                console.error("Registration failed:", registrationError);
                setError(`Registration failed: ${registrationError.message}`);
                actions.setSubmitting(false);
                return;
            }
        }
        console.log("Authenticated...");

        try {
            // Create shipping information
            console.log("Creating shipping information...");

            const shippingInfo = {
                user_id: currentUser.id,
                address_line1: values.addressLine1,
                address_line2: values.addressLine2 || "",
                city: values.city,
                state: values.state,
                postal_code: values.zip,
                country: values.country,
                phone_number: values.phoneNumber,
            };

            const shippingResponse = await fetch("/shipping_info", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(shippingInfo),
            });
            if (!shippingResponse.ok) {
                throw new Error("Failed to fetch shipping information.");
            }

            const shippingData = await shippingResponse.json();
            console.log(shippingData);
            const shippingInfoId = shippingData.id;
            console.log(
                "Shipping information created successfully",
                shippingData
            );
            console.log("Creating order with order details");

            const orderDetails = cartItems.map((item) => ({
                product_id: item.id,
                quantity: item.quantity,
                color_id: item.colorId,
            }));

            const orderResponse = await fetch("/orders", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    shipping_info_id: shippingInfoId,
                    confirmation_num: uuidv4(),
                    order_details: orderDetails,
                }),
            });
            if (!orderResponse.ok) {
                throw new Error("Failed to create order.");
            }
            const orderData = await orderResponse.json();
            console.log("Order created successfully", orderData);
            actions.setSubmitting(false);
            history.push("/confirmation");
        } catch (error) {
            console.error("Checkout process error:", error);
            setError(`Checkout process failed: ${error.message}`);
            actions.setSubmitting(false);
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Checkout</h1>
            {error && <div className="text-red-500">{error}</div>}

            <div className="mb-6">
                {cartItems.map((item) => (
                    <div
                        key={item.id}
                        className="flex justify-between items-center bg-white p-4 rounded-md mb-2 shadow"
                    >
                        <div className="flex items-center">
                            <img
                                className="w-16 h-16 object-cover rounded mr-4"
                                src={`/static/${item.image_path}`}
                                alt={item.name}
                            />
                            <div>
                                <h5 className="font-bold">{item.name}</h5>
                                <p className="text-sm text-gray-500">
                                    Quantity: {item.quantity}
                                </p>
                                <p className="text-sm text-gray-500">
                                    Color: {item.color}{" "}
                                </p>
                            </div>
                        </div>
                        <span className="font-semibold">
                            ${((item.price * item.quantity) / 100).toFixed(2)}
                        </span>
                    </div>
                ))}
                <p className="text-xl font-bold">Total: ${calculateTotal()}</p>
            </div>

            <Formik
                initialValues={{
                    firstName: "",
                    lastName: "",
                    addressLine1: "",
                    addressLine2: "",
                    city: "",
                    state: "",
                    zip: "",
                    country: "",
                    phoneNumber: "",
                    email: "",
                    username: "",
                    password: "",
                }}
                validationSchema={CheckoutSchema}
                onSubmit={handleFormSubmit}
            >
                {({ isSubmitting, errors, touched }) => (
                    <Form className="bg-white p-4 rounded-md shadow">
                        <div className="grid gap-4 sm:grid-cols-2 mb-4">
                            {/* First Name */}
                            <div>
                                <label
                                    htmlFor="firstName"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    First Name
                                </label>
                                <Field
                                    id="firstName"
                                    name="firstName"
                                    placeholder="First Name"
                                    className="p-2 border rounded mt-1"
                                    autoComplete="given-name"
                                />
                                {errors.firstName && touched.firstName ? (
                                    <div className="text-red-500">
                                        {errors.firstName}
                                    </div>
                                ) : null}
                            </div>
                            {/* Last Name */}
                            <div>
                                <label
                                    htmlFor="lastName"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    Last Name
                                </label>
                                <Field
                                    id="lastName"
                                    name="lastName"
                                    placeholder="Last Name"
                                    className="p-2 border rounded mt-1"
                                    autoComplete="family-name"
                                />
                                {errors.lastName && touched.lastName ? (
                                    <div className="text-red-500">
                                        {errors.lastName}
                                    </div>
                                ) : null}
                            </div>
                        </div>
                        {/* Address Line 1 */}
                        <div>
                            <label
                                htmlFor="addressLine1"
                                className="block text-sm font-medium text-gray-700"
                            >
                                Address Line 1
                            </label>
                            <Field
                                id="addressLine1"
                                name="addressLine1"
                                placeholder="Address Line 1"
                                className="p-2 border rounded mt-1 w-full"
                                autoComplete="address-line1"
                            />
                            {errors.addressLine1 && touched.addressLine1 ? (
                                <div className="text-red-500">
                                    {errors.addressLine1}
                                </div>
                            ) : null}
                        </div>
                        {/* Address Line 2 */}
                        <div>
                            <label
                                htmlFor="addressLine2"
                                className="block text-sm font-medium text-gray-700"
                            >
                                Address Line 2
                            </label>
                            <Field
                                id="addressLine2"
                                name="addressLine2"
                                placeholder="Address Line 2 (Optional)"
                                className="p-2 border rounded mt-1 w-full"
                                autoComplete="address-line2"
                            />
                            {errors.addressLine2 && touched.addressLine2 ? (
                                <div className="text-red-500">
                                    {errors.addressLine2}
                                </div>
                            ) : null}
                        </div>
                        <div className="grid gap-4 sm:grid-cols-3 mb-4">
                            {/* City */}
                            <div>
                                <label
                                    htmlFor="city"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    City
                                </label>
                                <Field
                                    id="city"
                                    name="city"
                                    placeholder="City"
                                    className="p-2 border rounded mt-1"
                                    autoComplete="address-level2"
                                />
                                {errors.city && touched.city ? (
                                    <div className="text-red-500">
                                        {errors.city}
                                    </div>
                                ) : null}
                            </div>
                            {/* State */}
                            <div>
                                <label
                                    htmlFor="state"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    State
                                </label>
                                <Field
                                    id="state"
                                    name="state"
                                    placeholder="State"
                                    className="p-2 border rounded mt-1"
                                    autoComplete="address-level1"
                                />
                                {errors.state && touched.state ? (
                                    <div className="text-red-500">
                                        {errors.state}
                                    </div>
                                ) : null}
                            </div>
                            {/* ZIP / Postal Code */}
                            <div>
                                <label
                                    htmlFor="zip"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    ZIP / Postal Code
                                </label>
                                <Field
                                    id="zip"
                                    name="zip"
                                    placeholder="ZIP / Postal Code"
                                    className="p-2 border rounded mt-1"
                                    autoComplete="postal-code"
                                />
                                {errors.zip && touched.zip ? (
                                    <div className="text-red-500">
                                        {errors.zip}
                                    </div>
                                ) : null}
                            </div>
                        </div>
                        {/* Country */}
                        <div>
                            <label
                                htmlFor="country"
                                className="block text-sm font-medium text-gray-700"
                            >
                                Country
                            </label>
                            <Field
                                id="country"
                                name="country"
                                placeholder="Country"
                                className="p-2 border rounded mt-1 w-full"
                                autoComplete="country-name"
                            />
                            {errors.country && touched.country ? (
                                <div className="text-red-500">
                                    {errors.country}
                                </div>
                            ) : null}
                        </div>
                        {/* Phone Number */}
                        <div>
                            <label
                                htmlFor="phoneNumber"
                                className="block text-sm font-medium text-gray-700"
                            >
                                Phone Number
                            </label>
                            <Field
                                id="phoneNumber"
                                name="phoneNumber"
                                placeholder="Phone Number"
                                className="p-2 border rounded mt-1 w-full"
                                autoComplete="tel"
                            />
                            {errors.phoneNumber && touched.phoneNumber ? (
                                <div className="text-red-500">
                                    {errors.phoneNumber}
                                </div>
                            ) : null}
                        </div>
                        {/* Email, Username, Password (conditional rendering based on authentication state) */}
                        {!isAuthenticated && (
                            <>
                                <div>
                                    <label
                                        htmlFor="email"
                                        className="block text-sm font-medium text-gray-700"
                                    >
                                        Email
                                    </label>
                                    <Field
                                        id="email"
                                        name="email"
                                        type="email"
                                        placeholder="Email"
                                        className="p-2 border rounded mt-1 w-full"
                                        autoComplete="email"
                                    />
                                    {errors.email && touched.email ? (
                                        <div className="text-red-500">
                                            {errors.email}
                                        </div>
                                    ) : null}
                                </div>
                                <div>
                                    <label
                                        htmlFor="username"
                                        className="block text-sm font-medium text-gray-700"
                                    >
                                        Username
                                    </label>
                                    <Field
                                        id="username"
                                        name="username"
                                        placeholder="Username"
                                        className="p-2 border rounded mt-1 w-full"
                                        autoComplete="username"
                                    />
                                    {errors.username && touched.username ? (
                                        <div className="text-red-500">
                                            {errors.username}
                                        </div>
                                    ) : null}
                                </div>
                                <div>
                                    <label
                                        htmlFor="password"
                                        className="block text-sm font-medium text-gray-700"
                                    >
                                        Password
                                    </label>
                                    <Field
                                        id="password"
                                        name="password"
                                        type="password"
                                        placeholder="Password"
                                        className="p-2 border rounded mt-1 w-full"
                                        autoComplete="new-password"
                                    />
                                    {errors.password && touched.password ? (
                                        <div className="text-red-500">
                                            {errors.password}
                                        </div>
                                    ) : null}
                                </div>
                            </>
                        )}
                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
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
