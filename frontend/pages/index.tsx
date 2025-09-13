import React, { useState } from 'react'

export default function Home() {
  const [query, setQuery] = useState('{"origin":"LON","when":"next week","prefs":["warm","beach","old town"],"max_flight_hours":2}')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const api = process.env.NEXT_PUBLIC_API || 'http://localhost:8000'

  const submit = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${api}/itinerary/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: query,
      })
      const json = await res.json()
      setResult(json)
    } catch (e) {
      setResult({ error: String(e) })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', padding: 24 }}>
      <h1>TripWeaver</h1>
      <p>Enter a JSON query (example prefilled) and click Plan</p>
      <textarea style={{width: '100%', height: 120}} value={query} onChange={(e)=>setQuery(e.target.value)} />
      <div style={{marginTop:12}}>
        <button onClick={submit} disabled={loading}>Plan</button>
      </div>
      <div style={{marginTop:24}}>
        {loading && <div>Loading...</div>}
        {result && <pre style={{background:'#f6f6f6', padding:12}}>{JSON.stringify(result, null, 2)}</pre>}
      </div>
    </div>
  )
}
