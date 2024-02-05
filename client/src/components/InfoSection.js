import React from "react";
import "../index.css";

function InfoSection() {
    // Static information for the three columns
    const staticFeatures = [
        {
            title: "User-Friendly Design",
            description:
                "Designed with the user in mind, our FuturePhone model offers an intuitive interface that simplifies your life.",
        },
        {
            title: "Sustainable Solutions",
            description:
                "We're committed to sustainability, using eco-friendly materials and processes to protect our planet.",
        },
        {
            title: "Cutting-Edge Performance",
            description:
                "Experience unparalleled performance and speed with the latest technology packed into every FuturePhone.",
        },
    ];

    return (
        <div className="bg-coolGray py-16">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 text-center">
                    {/* Static Content Columns */}
                    {staticFeatures.map((staticFeature, index) => (
                        <div key={index} className="lg:col-span-1">
                            <h3 className="text-xl font-bold text-gray-800 mb-2">
                                {staticFeature.title}
                            </h3>
                            <p className="text-base text-gray-600">
                                {staticFeature.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default InfoSection;
