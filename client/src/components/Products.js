import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Products() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await fetch("/product");
                if (!response.ok) {
                    throw new Error("Error fetching products");
                }
                const responseData = await response.json();

                const productsArray = responseData.products
                    ? responseData.products
                    : [];
                setProducts(productsArray);
            } catch (error) {
                console.error("Error fetching products:", error);
            }
        };

        fetchProducts();
    }, []);

    return (
        <div className="bg-coolGray">
            {/* Products grid */}
            <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
                <h2 className="sr-only">Products</h2>
                <div className="grid grid-cols-1 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
                    {products.map((product) => {
                        const formattedPrice = `$${product.price.toFixed(2)}`;
                        return (
                            <Link
                                key={product.id}
                                to={`/productdetail/${product.id}`}
                                className="group"
                            >
                                <div className="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-lg bg-gray-200">
                                    <img
                                        src={`/static/${product.image_path}`}
                                        alt={product.imageAlt}
                                        className="h-full w-full object-cover object-center group-hover:opacity-75"
                                    />
                                </div>
                                <h3 className="mt-4 text-sm text-gray-700">
                                    {product.name}
                                </h3>
                                {/* Display the formatted price */}
                                <p className="mt-1 text-lg font-medium text-gray-900">
                                    {formattedPrice}
                                </p>
                            </Link>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
