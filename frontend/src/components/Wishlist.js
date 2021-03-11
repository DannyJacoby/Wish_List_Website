const Wishlist = ({ wishlist }) => {
    return (
        <div className='wishlist'>
            <h3>{wishlist.text}
            </h3>
            <p>{wishlist.category}</p>
        </div>
    )
}

export default Wishlist