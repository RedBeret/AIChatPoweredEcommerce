import React from "react";
import visionXPhoneImage from "../assets/img/visionxhalo.png";
const features = [
    { name: "Origin", description: "Designed by FuturePhone Inc." },
    {
        name: "Material",
        description:
            "Solid frame with integrated AI technology for holographic displays",
    },
    { name: "Dimensions", description: '5.8" x 2.7" x 0.3"' },
    {
        name: "Finish",
        description: "Precision-milled aluminum with a matte finish",
    },
    {
        name: "Includes",
        description: "VisionX phone, USB-C charger, and user manual",
    },
    {
        name: "Considerations",
        description:
            "Built with sustainable materials. Eco-friendly manufacturing process.",
    },
];

export default function InfoSection2() {
    return (
        <div className="bg-white">
            <div className="mx-auto grid max-w-2xl grid-cols-1 items-center gap-x-8 gap-y-16 px-4 py-24 sm:px-6 sm:py-32 lg:max-w-7xl lg:grid-cols-2 lg:px-8">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                        Technical Specifications
                    </h2>
                    <p className="mt-4 text-gray-500">
                        VisionX phone is designed to bring the future to your
                        fingertips, featuring a sleek design and
                        state-of-the-art technology for an unparalleled user
                        experience.
                    </p>

                    <dl className="mt-16 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 sm:gap-y-16 lg:gap-x-8">
                        {features.map((feature) => (
                            <div
                                key={feature.name}
                                className="border-t border-gray-200 pt-4"
                            >
                                <dt className="font-medium text-gray-900">
                                    {feature.name}
                                </dt>
                                <dd className="mt-2 text-sm text-gray-500">
                                    {feature.description}
                                </dd>
                            </div>
                        ))}
                    </dl>
                </div>
                <div>
                    <img
                        src={visionXPhoneImage}
                        alt="VisionX phone showcasing its holographic display technology."
                        className="w-full h-auto object-cover rounded-lg bg-gray-100"
                    />
                </div>
            </div>
        </div>
    );
}
