import Button from './Button'

const Header = ({ title }) => {
    const onClick = () => {
        console.log('Click')
    }

    return (
        <header className='header'>
            <h1>{title}</h1>
            <Button color='lightblue' text='Add' onClick=
            {onClick}/>
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