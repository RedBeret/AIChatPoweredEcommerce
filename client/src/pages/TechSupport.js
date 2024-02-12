import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { sendMessage } from "../store/actions/chatActions";

export default function TechSupport() {
    const [message, setMessage] = useState("");
    const dispatch = useDispatch();
    const messages = useSelector((state) => state.chat.messages);
    const [textAreaRows, setTextAreaRows] = useState(1);
    const AccessibleFontStyle = {
        fontFamily: '"Open Dyslexic", sans-serif',
    };
    const handleSendMessage = (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        dispatch(sendMessage(message));
        setMessage("");
    };

    const renderMessage = (msg, index) => {
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
    const handleTextAreaChange = (e) => {
        setMessage(e.target.value);
        const numberOfRows = e.target.value.split("\n").length;
        setTextAreaRows(numberOfRows > 3 ? 3 : numberOfRows);
    };
    return (
        <div
            className="flex flex-col h-screen justify-between bg-coolGray text-black"
            style={AccessibleFontStyle}
        >
            {/* Content Area */}
            <div className="flex flex-grow  justify-center p-4">
                <div className="m-4 md:mx-20 md:my-8 p-4 max-w-7xl mx-auto sm:px-6 lg:px-8 flex bg-white shadow rounded-lg flex-grow">
                    {/* Chat Area */}
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
            </div>
            {/* Input Area */}
            <div className="p-4 fixed inset-x-0 bottom-0 bg-white shadow-lg">
                <div className="mx-4 md:mx-20 mb-8 p-4 bg-white rounded-lg">
                    <form
                        onSubmit={handleSendMessage}
                        className="flex items-center"
                    >
                        <textarea
                            value={message}
                            onChange={handleTextAreaChange}
                            placeholder="Type your message..."
                            className="flex-1 p-2 border border-gray-300 rounded-md resize-none"
                            rows={textAreaRows}
                            style={{ minHeight: "38px", maxHeight: "76px" }}
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
