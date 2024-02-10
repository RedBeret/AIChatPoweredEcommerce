import React, { useState } from "react";

export default function TechSupport() {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (!message.trim()) return;
        setMessages([
            ...messages,
            { id: messages.length + 1, text: message, sender: "user" },
            {
                id: messages.length + 2,
                text: "Your message has been received.",
                sender: "support",
            },
        ]);
        setMessage("");
    };

    const renderMessage = (msg) => {
        if (msg.sender === "user") {
            return (
                <div key={msg.id} className="flex items-center my-2">
                    <span className="text-lg">🙋‍♂️</span>
                    <div className="ml-2 p-2 bg-blue-200 rounded-lg">
                        {msg.text}
                    </div>
                </div>
            );
        } else {
            return (
                <div
                    key={msg.id}
                    className="flex items-center justify-end my-2"
                >
                    <div className="mr-2 p-2 bg-green-200 rounded-lg">
                        {msg.text}
                    </div>
                    <span className="text-lg">🤖</span>
                </div>
            );
        }
    };

    return (
        <div className="flex flex-col h-screen justify-between bg-gray-100">
            {/* Content Area */}
            <div className="m-4 md:mx-20 md:my-8 p-4 bg-white shadow rounded-lg flex-grow">
                {/* ... other content ... */}
                <div className="flex-grow mt-8 mb-16 overflow-y-auto">
                    <h2 className="text-xl font-semibold">
                        Chat with VisionX AI
                    </h2>
                    <div className="mt-4 p-4 bg-gray-100 rounded-lg max-h-[calc(100vh-16rem)] overflow-y-auto">
                        {messages.map(renderMessage)}
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
