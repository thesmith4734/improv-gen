import './App.css';
import GameList from './components';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        Improv Games:
        <GameList items={["What are you doing?", "Switch Interview", "Countdown"]} />
      </header>
    </div>
  );
}

export default App;
