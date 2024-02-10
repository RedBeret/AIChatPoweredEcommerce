import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { sendMessage } from "../store/actions/chatActions";

export default function TechSupport() {
    const [message, setMessage] = useState("");
    const dispatch = useDispatch();
    const { messages, error, success } = useSelector((state) => state.chat);

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        dispatch(sendMessage(message));
        setMessage("");
    };

    const renderMessage = (msg, index) => {
        const key = msg.id || index;
        return (
            <div
                key={key}
                className={`flex items-center my-2 ${
                    msg.sender === "user" ? "" : "justify-end"
                }`}
            >
                <div
                    className={`p-2 rounded-lg ${
                        msg.sender === "user" ? "bg-blue-200" : "bg-green-200"
                    }`}
                >
                    {msg.text}
                </div>
                <span className="text-lg">
                    {msg.sender === "user" ? "🙋‍♂️" : "🤖"}
                </span>
            </div>
        );
    };
    return (
        <div className="flex flex-col h-screen justify-between bg-gray-100">
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}{" "}
            {success && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{success}</span>
                </div>
            )}{" "}
            {/* Content Area */}
            <div className="m-4 md:mx-20 md:my-8 p-4 bg-white shadow rounded-lg flex-grow">
                {/* ... other content ... */}
                <div className="flex-grow mt-8 mb-16 overflow-y-auto">
                    <h2 className="text-xl font-semibold">
                        Chat with VisionX AI
                    </h2>
                    <div className="mt-4 p-4 bg-gray-100 rounded-lg max-h-[calc(100vh-16rem)] overflow-y-auto">
                        {messages.map((msg, index) =>
                            renderMessage(msg, index)
                        )}
                    </div>
                </div>
            </div>
            {/* Input Area */}
            <div className="p-4 fixed inset-x-0 bottom-0 bg-white shadow-lg">
                <div className="m-4 md:mx-20 md:mb-8 p-4 bg-white rounded-lg">
                    <form
                        onSubmit={handleSendMessage}
                        className="flex items-center"
                    >
                        <textarea
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Type your message..."
                            className="flex-1 p-2 border border-gray-300 rounded-md resize-none"
                            rows="1"
                        ></textarea>
                        <button
                            type="submit"
                            className="ml-4 p-2 bg-blue-500 text-white rounded-md"
                        >
                            Send
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
