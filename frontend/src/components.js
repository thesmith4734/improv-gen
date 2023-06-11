export default function GameList(props) {
    const listGames = props.items.map(
        (item, index) => (<li key={index}>{item}</li>)
    );
    return (
        <ul>
            {listGames}
        </ul>
    );
}