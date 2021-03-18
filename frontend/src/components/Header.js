

const Header = ({ title }) => {

    return (
        <header className='header'>
            <h1>{title}</h1>
        </header>
    )
}

Header.defaultProps = {
    title: 'Wishlist App',
}

const headingStyle = {
    color: 'red', 
    backgroundColor: 'black'
}

export default Header