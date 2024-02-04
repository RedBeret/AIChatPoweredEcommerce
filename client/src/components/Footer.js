// Footer.js
import React from "react";
import logo from "../assets/img/vision_x_logo.png";
import { Link } from "react-router-dom";

export default function Footer() {
    return (
        <footer className="bg-coolGray dark:bg-coolGray">
            <div className="container px-6 py-12 mx-auto">
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                    {/* Support Section */}
                    <div>
                        <p className="font-semibold text-gray-800 dark:text-black">
                            Support
                        </p>
                        <ul className="mt-4 space-y-2">
                            <li>
                                <span
                                    role="button"
                                    tabIndex="0"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer"
                                >
                                    Shipping & Returns
                                </span>
                            </li>
                            <li>
                                <span
                                    role="button"
                                    tabIndex="0"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer"
                                >
                                    Warranty
                                </span>
                            </li>
                            <li>
                                <span
                                    role="button"
                                    tabIndex="0"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer"
                                >
                                    FAQ
                                </span>
                            </li>
                        </ul>
                    </div>

                    {/* Quick Links Section */}
                    <div>
                        <p className="font-semibold text-gray-800 dark:text-black">
                            Quick Links
                        </p>
                        <ul className="mt-4 space-y-2">
                            <li>
                                <Link
                                    to="/"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Home
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/about"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    About
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/contact"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Contact
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Social Icons Section */}
                    <div>
                        <p className="font-semibold text-gray-800 dark:text-black">
                            Follow Us
                        </p>
                        <ul className="flex items-center mt-4 space-x-4">
                            <a
                                href="https://github.com/RedBeret"
                                className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                            >
                                <svg
                                    className="w-5 h-5 fill-current"
                                    viewBox="0 0 24 24"
                                >
                                    {/* GitHub SVG Path */}
                                    <path
                                        fill="currentColor"
                                        d="M12 .297c-6.6 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.607-4.042-1.607-.546-1.387-1.332-1.755-1.332-1.755-1.09-.745.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.694.825.577C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
                                    ></path>
                                </svg>
                            </a>
                        </ul>
                    </div>

                    {/* User Management Section */}
                    <div>
                        <p className="font-semibold text-gray-800 dark:text-black">
                            User Management
                        </p>
                        <ul className="mt-4 space-y-2">
                            <li>
                                <Link
                                    to="/login"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Log In
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/signup"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Sign Up
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/updatepassword"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Update Account
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/deleteuser"
                                    className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400"
                                >
                                    Delete Account
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                <hr className="my-6 border-gray-200 dark:border-gray-700" />

                <div className="flex items-center justify-between">
                    {/* Company Logo and Name is here */}
                    <button className="flex items-center">
                        <img
                            className="w-auto h-8"
                            src={logo}
                            alt="VisionX Logo"
                        />
                        <span className="ml-3 text-xl font-semibold text-black">
                            VisionX Company
                        </span>
                    </button>

                    {/* Bottom Links */}
                    <div className="flex items-center space-x-4">
                        <span className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer">
                            Privacy Policy
                        </span>
                        <span className="text-gray-600 hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer">
                            Terms of Service
                        </span>
                    </div>
                </div>
            </div>
        </footer>
    );
}
