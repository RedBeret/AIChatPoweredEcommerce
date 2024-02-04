import React from "react";
import { Link } from "react-router-dom";
import { Typewriter } from "react-simple-typewriter";
import visionXPhoneImage from "../assets/img/visionxphone.png";

function HeroSection() {
    return (
        <div className="bg-white dark:bg-phoneBg">
            <div className="border-b dark:border-gray-700">
                <div className="container m-auto px-6 pt-24 md:px-12 lg:pt-[4.8rem] lg:px-7">
                    <div className="grid lg:grid-cols-2 items-center gap-12 px-2 md:px-0">
                        <div className="col-span-1">
                            <div className="relative w-full">
                                <img
                                    src={visionXPhoneImage}
                                    alt="VisionX Phone"
                                    loading="lazy"
                                />
                            </div>
                        </div>

                        <div className="relative col-span-1">
                            <h1 className="font-bold text-5xl sm:text-6xl md:text-7xl xl:text-8xl dark:text-white">
                                Your Forever
                            </h1>
                            <h1 className="font-bold text-5xl sm:text-6xl md:text-7xl xl:text-8xl dark:text-white">
                                <span className="inline-block text-cyan-500">
                                    <Typewriter
                                        words={[
                                            "Future",
                                            "Companion",
                                            "Life",
                                            "Phone",
                                        ]}
                                        loop={Infinity}
                                        cursor
                                        cursorStyle="|"
                                        typeSpeed={240}
                                        deleteSpeed={100}
                                        delaySpeed={1000}
                                    />
                                </span>
                            </h1>
                            <div className="mt-8 lg:mt-16 space-y-8">
                                <p className="text-gray-700 dark:text-gray-300">
                                    Experience the pinnacle of smartphone
                                    technology. Upgrade to the new era with our
                                    one-hour in-store part upgrades, embracing
                                    both luxury and eco-consciousness.
                                </p>
                                <div className="flex space-x-4 mt-6">
                                    <Link
                                        to="/productdetail/1"
                                        className="w-full py-3 px-6 text-center rounded-full transition duration-300 bg-gray-900 dark:bg-gray-700 hover:bg-cyan-500 active:bg-cyan-600 focus:bg-cyan-800 sm:w-max mb-4 text-white text-sm"
                                        title="Buy now"
                                    >
                                        Buy now
                                    </Link>
                                    <Link
                                        to="/productdetail/1"
                                        className="w-full py-3 px-6 text-center rounded-full transition border border-gray-200 dark:border-gray-700 sm:w-max mb-4 text-gray-800 text-sm dark:text-white"
                                        title="View phone"
                                    >
                                        View phone
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default HeroSection;
