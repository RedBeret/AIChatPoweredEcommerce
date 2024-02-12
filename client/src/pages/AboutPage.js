import React from "react";
import {
    CloudArrowUpIcon,
    LockClosedIcon,
    ServerIcon,
} from "@heroicons/react/20/solid";
import FuturePhoneImage from "../assets/img/visionxphone.png";

function About() {
    return (
        <div className="relative isolate overflow-hidden bg-white px-6 py-24 sm:py-32 lg:overflow-visible lg:px-0">
            <div className="absolute inset-0 -z-10 overflow-hidden">
                {/* Background pattern and styling */}
                <svg
                    className="absolute left-[max(50%,25rem)] top-0 h-[64rem] w-[128rem] -translate-x-1/2 stroke-gray-200 [mask-image:radial-gradient(64rem_64rem_at_top,white,transparent)]"
                    aria-hidden="true"
                >
                    {/* SVG Pattern */}
                    <defs>
                        <pattern
                            id="e813992c-7d03-4cc4-a2bd-151760b470a0"
                            width={200}
                            height={200}
                            x="50%"
                            y={-1}
                            patternUnits="userSpaceOnUse"
                        >
                            <path d="M100 200V.5M.5 .5H200" fill="none" />
                        </pattern>
                    </defs>
                    <rect
                        width="100%"
                        height="100%"
                        strokeWidth={0}
                        fill="url(#e813992c-7d03-4cc4-a2bd-151760b470a0)"
                    />
                </svg>
            </div>
            {/* Main content grid */}
            <div className="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 lg:mx-0 lg:max-w-none lg:grid-cols-2 lg:items-start lg:gap-y-10">
                <div className="lg:col-span-2 lg:col-start-1 lg:row-start-1 lg:mx-auto lg:grid lg:w-full lg:max-w-7xl lg:grid-cols-2 lg:gap-x-8 lg:px-8">
                    <div className="lg:pr-4">
                        <div className="lg:max-w-lg">
                            {/* Updated company introduction */}
                            <p className="text-base font-semibold leading-7 text-indigo-600">
                                About FuturePhone Inc.
                            </p>
                            <h1 className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                                Innovating Communication
                            </h1>
                            <p className="mt-6 text-xl leading-8 text-gray-700">
                                At FuturePhone Inc., we're dedicated to
                                revolutionizing communication with our
                                state-of-the-art, user-friendly, and sustainable
                                smartphone technology. Our commitment to
                                innovation, quality, and sustainability ensures
                                that we continue to offer cutting-edge solutions
                                that enhance connectivity and user experience.
                            </p>
                        </div>
                    </div>
                </div>
                <div className="-ml-12 -mt-12 p-12 lg:sticky lg:top-4 lg:col-start-2 lg:row-span-2 lg:row-start-1 lg:overflow-hidden">
                    {/* Adjusted image size with TailwindCSS */}
                    <img
                        className="max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg rounded-xl bg-gray-900 shadow-xl ring-1 ring-gray-400/10"
                        src={FuturePhoneImage}
                        alt="FuturePhone Inc. flagship smartphone"
                    />
                </div>
                <div className="lg:col-span-2 lg:col-start-1 lg:row-start-2 lg:mx-auto lg:grid lg:w-full lg:max-w-7xl lg:grid-cols-2 lg:gap-x-8 lg:px-8">
                    <div className="lg:pr-4">
                        <div className="max-w-xl text-base leading-7 text-gray-700 lg:max-w-lg">
                            {/* Detailed information about company values and approach */}
                            <p>
                                Our journey began in 2010 with a clear mission:
                                to enhance how people communicate across the
                                globe. Through our flagship smartphones,
                                proprietary software, and unmatched customer
                                support, we aim to provide an unparalleled user
                                experience. Our dedication to sustainability and
                                customer-centricity is reflected in every
                                product we design and every interaction we have.
                            </p>
                            {/* Highlighting core values with icons */}
                            <ul
                                role="list"
                                className="mt-8 space-y-8 text-gray-600"
                            >
                                <li className="flex gap-x-3">
                                    <CloudArrowUpIcon
                                        className="mt-1 h-5 w-5 flex-none text-indigo-600"
                                        aria-hidden="true"
                                    />
                                    <span>
                                        <strong className="font-semibold text-gray-900">
                                            Innovation at Every Step.
                                        </strong>{" "}
                                        From AI-powered functionalities to
                                        eco-friendly manufacturing processes,
                                        our commitment to innovation drives us
                                        forward.
                                    </span>
                                </li>
                                <li className="flex gap-x-3">
                                    <LockClosedIcon
                                        className="mt-1 h-5 w-5 flex-none text-indigo-600"
                                        aria-hidden="true"
                                    />
                                    <span>
                                        <strong className="font-semibold text-gray-900">
                                            Uncompromised Security.
                                        </strong>{" "}
                                        We prioritize your privacy and data
                                        security, integrating top-of-the-line
                                        security features into our devices.
                                    </span>
                                </li>
                                <li className="flex gap-x-3">
                                    <ServerIcon
                                        className="mt-1 h-5 w-5 flex-none text-indigo-600"
                                        aria-hidden="true"
                                    />
                                    <span>
                                        <strong className="font-semibold text-gray-900">
                                            Sustainability First.
                                        </strong>{" "}
                                        Our approach to sustainability ensures
                                        that we not only lead with innovation
                                        but also with responsibility towards our
                                        planet.
                                    </span>
                                </li>
                            </ul>
                            <p className="mt-8">
                                By embracing these values, FuturePhone Inc.
                                continues to set the standard for excellence and
                                sustainability in the smartphone industry. Join
                                us as we push the boundaries of technology,
                                creating a future where communication is
                                limitless.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default About;
