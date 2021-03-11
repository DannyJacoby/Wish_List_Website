import Wishlist from './Wishlist'

const Wishlists = ({ wishlists }) => {
    return (
        <>
          {wishlists.map((wishlist) => (
          <Wishlist key={wishlist.id} wishlist={wishlist} />
          ))}  
        </>
    )
}

export default Wishlists