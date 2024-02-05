import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { fetchProducts } from "../store/actions/productActions";

export default function Products() {
    const dispatch = useDispatch();
    // Correctly access the state under the 'products' key, and then directly use the productList
    const { productList, isLoading, error } = useSelector(
        (state) => state.products
    );

    useEffect(() => {
        dispatch(fetchProducts());
    }, [dispatch]);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    return (
        <div className="bg-coolGray">
            {/* Products grid */}
            <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
                <h2 className="sr-only">Products</h2>
                <div className="grid grid-cols-1 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
                    {productList.map((product) => {
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
