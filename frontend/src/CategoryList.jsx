function CategoryList({ categories }) {
    return (
        <>
            <h2>Categories</h2>

            {categories.length === 0 ? (
                <p>No categories found.</p>
            ) : (
                <ul className="category-list">
                    {categories.map((category) => (
                        <li
                            key={category.id}
                            className="category-item"
                        >
                            {category.name}
                        </li>
                    ))}
                </ul>
            )}
        </>
    );
}

export default CategoryList;