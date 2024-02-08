import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { StarIcon } from "@heroicons/react/20/solid";
import { useCartContext } from "../components/CartContext";
import { RadioGroup } from "@headlessui/react";
import { useDispatch, useSelector } from "react-redux";
import { fetchProduct } from "../store/actions/productActions";

function classNames(...classes) {
    return classes.filter(Boolean).join(" ");
}

export default function ProductDetail() {
    const { id } = useParams();
    const dispatch = useDispatch();
    const product = useSelector((state) => state.products.selectedProduct);
    const isLoading = useSelector((state) => state.products.isLoading);
    const error = useSelector((state) => state.products.error);
    const { addToCart } = useCartContext();
    const [selectedColor, setSelectedColor] = useState("");

    useEffect(() => {
        dispatch(fetchProduct(id));
    }, [dispatch, id]);

    if (error) {
        return <p className="text-center text-red-600">{error}</p>;
    }

    if (!product) {
        return <p className="text-center">Loading...</p>;
    }

    const formattedPrice = `$${(product.price / 100).toFixed(2)}`;

    return (
        <div className="bg-white py-8">
            {/* Check if loading */}
            {isLoading && <p className="text-center">Loading...</p>}

            {/* Check if there was an error */}
            {error && <p className="text-center text-red-600">{error}</p>}

            {/* Only display product details if not loading and there's no error */}
            {!isLoading && !error && product && (
                /* Product details */
                <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:grid lg:grid-cols-3 lg:gap-x-8 lg:px-8">
                    <div className="lg:col-span-1 flex justify-center lg:justify-start">
                        <img
                            src={`/static/${product.image_path}`}
                            alt={product.imageAlt}
                            className="rounded-lg shadow-md w-full lg:w-auto h-auto"
                        />
                    </div>
                    <div className="mt-4 lg:mt-0 lg:col-span-2">
                        <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
                            {product.name}
                        </h1>
                        <p className="mt-4 text-gray-900">
                            {product.description}
                        </p>
                        {/* Product rating and price */}
                        <div className="mt-6">
                            <div className="flex items-center">
                                {[0, 1, 2, 3, 4].map((rating) => (
                                    <StarIcon
                                        key={rating}
                                        className="text-blue-500 h-5 w-5 flex-shrink-0"
                                        aria-hidden="true"
                                    />
                                ))}
                            </div>
                            <p className="text-sm font-medium text-gray-600 mt-1">
                                Rated 5 stars by World Class Watch Raters
                            </p>
                        </div>

                        <p className="mt-1 text-lg font-medium text-gray-900">
                            {formattedPrice}
                        </p>
                        {/* Color selection */}
                        {product.colors.length > 0 && (
                            <div>
                                <h4 className="text-sm font-medium text-gray-900">
                                    Color
                                </h4>

                                <RadioGroup
                                    value={selectedColor}
                                    onChange={setSelectedColor}
                                    className="mt-4"
                                >
                                    <RadioGroup.Label className="sr-only">
                                        Choose a color
                                    </RadioGroup.Label>
                                    <div className="flex items-center space-x-3">
                                        {product.colors.map((color, index) => (
                                            <RadioGroup.Option
                                                key={index}
                                                value={color}
                                                className={({ checked }) =>
                                                    classNames(
                                                        "relative p-0.5 rounded-full flex items-center justify-center cursor-pointer focus:outline-none",
                                                        checked
                                                            ? "ring-2 ring-offset-2 ring-blue-500"
                                                            : "",
                                                        !checked
                                                            ? "ring-2 ring-transparent"
                                                            : ""
                                                    )
                                                }
                                            >
                                                <>
                                                    <span
                                                        className="inline-block h-8 w-8 rounded-full border border-black border-opacity-10"
                                                        style={{
                                                            backgroundColor:
                                                                color.name.toLowerCase() ===
                                                                "transparent"
                                                                    ? "transparent"
                                                                    : color.name.toLowerCase(),
                                                        }}
                                                    />
                                                    <span className="ml-2 text-sm font-medium text-gray-900">
                                                        {color.name}
                                                    </span>
                                                </>
                                            </RadioGroup.Option>
                                        ))}
                                    </div>
                                </RadioGroup>
                            </div>
                        )}
                        <button
                            onClick={() => addToCart(product, selectedColor)}
                            className="mt-10 w-full lg:w-auto flex items-center justify-center rounded-md border border-transparent bg-slate-600 px-8 py-3 text-base font-medium text-white hover:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        >
                            Add to Cart
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
