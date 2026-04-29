import React, { useState } from 'react'

export default function App() {
  const [secret, setSecret] = useState('')
  const [gameId, setGameId] = useState(null)
  const [guess, setGuess] = useState('')
  const [feedback, setFeedback] = useState(null)

  async function createGame() {
    const res = await fetch('/api/games', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secret })
    })
    const data = await res.json()
    setGameId(data.game_id)
    setFeedback(null)
  }

  async function sendGuess() {
    const res = await fetch(`/api/games/${gameId}/guess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guess })
    })
    const data = await res.json()
    setFeedback(data)
  }

  return (
    <div style={{ padding: 20, fontFamily: 'Arial' }}>
      <h1>Jogo da Adivinhação</h1>
      {!gameId ? (
        <div>
          <input placeholder="Senha (secreta)" value={secret} onChange={e => setSecret(e.target.value)} />
          <button onClick={createGame} disabled={!secret}>Criar Jogo</button>
        </div>
      ) : (
        <div>
          <p>Game ID: {gameId}</p>
          <input placeholder="Palpite" value={guess} onChange={e => setGuess(e.target.value)} />
          <button onClick={sendGuess} disabled={!guess}>Enviar Palpite</button>
        </div>
      )}
      {feedback && (
        <div style={{ marginTop: 12 }}>
          <pre>{JSON.stringify(feedback, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
