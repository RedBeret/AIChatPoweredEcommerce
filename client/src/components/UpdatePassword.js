import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Link, useHistory } from "react-router-dom";
import { updatePassword } from "../store/actions/authActions";

export default function UpdatePassword() {
    const history = useHistory();
    const dispatch = useDispatch();
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const initialValues = {
        username: "",
        currentPassword: "",
        newPassword: "",
        confirmNewPassword: "",
    };

    const validationSchema = Yup.object().shape({
        username: Yup.string().required("Required"),
        currentPassword: Yup.string().required("Required"),
        newPassword: Yup.string()
            .min(6, "Password must be at least 6 characters")
            .required("Required"),
        confirmNewPassword: Yup.string()
            .oneOf([Yup.ref("newPassword"), null], "Passwords must match")
            .required("Required"),
    });

    const onSubmit = (values, { setSubmitting }) => {
        const { username, currentPassword, newPassword } = values;
        dispatch(
            updatePassword(
                username,
                currentPassword,
                newPassword,
                setError,
                setSuccess,
                history
            )
        );
        setSubmitting(false);
    };
    return (
        <main className="w-full max-w-md mx-auto p-6">
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            {success && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{success}</span>
                </div>
            )}

            <div className="mt-7 bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-gray-800 dark:border-gray-700">
                <div className="p-4 sm:p-7">
                    <div className="text-center">
                        <h1 className="block text-2xl font-bold text-gray-800 dark:text-white">
                            Update Password
                        </h1>
                        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                            Back to{" "}
                            <Link
                                to="/"
                                className="text-blue-600 hover:underline font-medium dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                            >
                                Home
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
                                <Field
                                    name="username"
                                    type="text"
                                    placeholder="Username"
                                    className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                />
                                <ErrorMessage
                                    name="username"
                                    component="div"
                                    className="text-red-500 text-xs mt-1"
                                />

                                <Field
                                    name="currentPassword"
                                    type="password"
                                    placeholder="Current Password"
                                    className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                />
                                <ErrorMessage
                                    name="currentPassword"
                                    component="div"
                                    className="text-red-500 text-xs mt-1"
                                />

                                <Field
                                    name="newPassword"
                                    type="password"
                                    placeholder="New Password"
                                    className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                />
                                <ErrorMessage
                                    name="newPassword"
                                    component="div"
                                    className="text-red-500 text-xs mt-1"
                                />

                                <Field
                                    name="confirmNewPassword"
                                    type="password"
                                    placeholder="Confirm New Password"
                                    className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400"
                                />
                                <ErrorMessage
                                    name="confirmNewPassword"
                                    component="div"
                                    className="text-red-500 text-xs mt-1"
                                />

                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="w-full py-3 px-4 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-gray-600"
                                >
                                    Update Password
                                </button>
                            </Form>
                        )}
                    </Formik>
                </div>
            </div>
        </main>
    );
}
