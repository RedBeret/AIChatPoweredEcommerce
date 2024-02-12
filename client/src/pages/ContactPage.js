import React from "react";

function Contact() {
    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-4">Contact Us</h1>
            <div className="mb-8">
                <h2 className="text-2xl font-semibold">FuturePhone Inc.</h2>
                <p className="mt-2">
                    123 Tech Avenue, Silicon Valley, CA 94088
                </p>
                <p className="mt-1">
                    Email: ficticiouscontact@fakefuturephoneinc.com
                </p>
                <p>Phone: (123) 456-7890</p>
            </div>
            <div>
                <h2 className="text-2xl font-semibold mb-4">
                    Send Us a Message (Not Functional Yet! Under Maintenance!)
                </h2>
                <form>
                    <div className="mb-4">
                        <label
                            htmlFor="name"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Your Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            className="mt-1 p-2 w-full border border-gray-300 rounded-md shadow-sm"
                            placeholder="Your Name"
                        />
                    </div>
                    <div className="mb-4">
                        <label
                            htmlFor="email"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Your Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            className="mt-1 p-2 w-full border border-gray-300 rounded-md shadow-sm"
                            placeholder="Your Email"
                        />
                    </div>
                    <div className="mb-4">
                        <label
                            htmlFor="message"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Message
                        </label>
                        <textarea
                            id="message"
                            name="message"
                            rows="4"
                            className="mt-1 p-2 w-full border border-gray-300 rounded-md shadow-sm"
                            placeholder="Your message"
                        ></textarea>
                    </div>
                    <button
                        type="submit"
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    >
                        Send Message
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Contact;
