// client/src/pages/Home.js
import React from "react";
import Hero from "../components/Hero";
import InfoSection from "../components/InfoSection";
// import Products from "../components/Products";
import InfoSection2 from "../components/InfoSection2";
export default function Home() {
    return (
        <>
            <Hero />
            {/* <Products /> */}
            <InfoSection2 />
            <InfoSection />
        </>
    );
}
