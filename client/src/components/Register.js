import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Link, useHistory } from "react-router-dom";
import { registerUser } from "../store/actions/authActions";

export default function Register() {
    const dispatch = useDispatch();
    const history = useHistory();
    const [success, setSuccess] = useState("");
    const [error, setError] = useState("");
    const initialValues = {
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
    };

    const validationSchema = Yup.object().shape({
        email: Yup.string().email("Invalid email").required("Required"),
        username: Yup.string().required("Required"),
        password: Yup.string()
            .min(6, "Password must be at least 6 characters")
            .required("Required"),
        confirmPassword: Yup.string()
            .oneOf([Yup.ref("password"), null], "Passwords must match")
            .required("Required"),
    });

    const onSubmit = (values, { setSubmitting }) => {
        setError("");

        dispatch(
            registerUser(
                values,
                setError,
                (message) => {
                    setSuccess(message);
                    setTimeout(() => {
                        history.push("/");
                    }, 2000);
                },
                history
            )
        );
        setSubmitting(false);
    };

    return (
        <main className="w-full max-w-md mx-auto p-6">
            {success && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
                    {success}
                </div>
            )}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                    {error}
                </div>
            )}
            <div className="mt-7 bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-gray-800 dark:border-gray-700">
                <div className="p-4 sm:p-7">
                    <div className="text-center">
                        <h1 className="block text-2xl font-bold text-gray-800 dark:text-white">
                            Sign up
                        </h1>
                        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                            Already have an account?{" "}
                            <Link
                                to="/auth/login"
                                className="text-blue-600 hover:underline font-medium dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                            >
                                Sign in here
                            </Link>
                        </p>
                    </div>

                    <Formik
                        initialValues={initialValues}
                        validationSchema={validationSchema}
                        onSubmit={onSubmit}
                    >
                        {({ isSubmitting }) => (
                            <Form className="mt-5">
                                <div className="mb-4">
                                    <label
                                        htmlFor="username"
                                        className="block text-sm font-medium text-gray-700 dark:text-gray-200"
                                    >
                                        Username
                                    </label>
                                    <Field
                                        id="username"
                                        name="username"
                                        type="text"
                                        placeholder="Username"
                                        autoComplete="username"
                                        className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                    />
                                    <ErrorMessage
                                        name="username"
                                        component="div"
                                        className="text-red-500 text-xs mt-1"
                                    />
                                </div>

                                <div className="mb-4">
                                    <label
                                        htmlFor="email"
                                        className="block text-sm font-medium text-gray-700 dark:text-gray-200"
                                    >
                                        Email
                                    </label>
                                    <Field
                                        id="email"
                                        name="email"
                                        type="email"
                                        placeholder="Email"
                                        autoComplete="email"
                                        className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                    />
                                    <ErrorMessage
                                        name="email"
                                        component="div"
                                        className="text-red-500 text-xs mt-1"
                                    />
                                </div>

                                <div className="mb-4">
                                    <label
                                        htmlFor="password"
                                        className="block text-sm font-medium text-gray-700 dark:text-gray-200"
                                    >
                                        Password
                                    </label>
                                    <Field
                                        id="password"
                                        name="password"
                                        type="password"
                                        placeholder="Password"
                                        autoComplete="new-password"
                                        className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                    />
                                    <ErrorMessage
                                        name="password"
                                        component="div"
                                        className="text-red-500 text-xs mt-1"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label
                                        htmlFor="confirmPassword"
                                        className="block text-sm font-medium text-gray-700 dark:text-gray-200"
                                    >
                                        Confirm Password
                                    </label>
                                    <Field
                                        id="confirmPassword"
                                        name="confirmPassword"
                                        type="password"
                                        placeholder="Confirm Password"
                                        autoComplete="new-password"
                                        className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                    />
                                    <ErrorMessage
                                        name="confirmPassword"
                                        component="div"
                                        className="text-red-500 text-xs mt-1"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="w-full py-3 px-4 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-gray-600"
                                >
                                    Sign up
                                </button>
                            </Form>
                        )}
                    </Formik>
                </div>
            </div>
        </main>
    );
}
