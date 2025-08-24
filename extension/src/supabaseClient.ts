import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://lmtuckpffvsgxyddxyer.supabase.co'; 
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxtdHVja3BmZnZzZ3h5ZGR4eWVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1NDcwMDIsImV4cCI6MjA3MTEyMzAwMn0.mgCIne5HhDzHy1oDvzjvk9Ex_yVgLbWBqsQQYg12PQA'; // This is the PUBLIC key

export const supabase = createClient(supabaseUrl, supabaseAnonKey);