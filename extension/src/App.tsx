import { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';
import { type Session } from '@supabase/supabase-js';

function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogin = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) alert(error.message);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab.id && tab.url?.includes('linkedin.com/jobs/view')) {
      try {
        const jobDetails = await chrome.tabs.sendMessage(tab.id, { type: 'GET_JOB_DETAILS' });
        const { data: { session } } = await supabase.auth.getSession();
        const token = session?.access_token;
        if (!token) {
          alert("Authentication error. Please log in again.");
          setIsLoading(false);
          return;
        }
        const response = await fetch('http://127.0.0.1:8000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            job_title: jobDetails.title,
            company_name: jobDetails.company,
            linkedin_url: tab.url,
            job_text: jobDetails.description
          })
        });

        if (response.ok) {
          alert("Analysis successful! Check your LinkSight dashboard.");
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        alert(`An error occurred: ${error instanceof Error ? error.message : "Unknown error"}`);
      }
    } else {
        alert("Please navigate to a LinkedIn job page to use this extension.");
    }
    setIsLoading(false);
  };

  if (!session) {
    return (
      <div className="container">
        <h2>Login to LinkSight AI</h2>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>LinkSight AI</h2>
      <p>Logged in as {session.user.email}</p>
      <button onClick={handleAnalyze} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Analyze this Job'}
      </button>
      <button onClick={() => supabase.auth.signOut()}>Logout</button>
    </div>
  );
}

export default App;