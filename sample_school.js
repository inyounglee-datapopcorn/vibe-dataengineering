const serviceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImloZW56dnl4bWxxbWZyd2pla25kIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMDI5OSwiZXhwIjoyMDc2MzA2Mjk5fQ.RutW3PGpnmT_slk9BDZGwqcfE9GghBM05wCjiEIYFkQ';
const url = 'https://ihenzvyxmlqmfrwjeknd.supabase.co';

async function main() {
    // Check school_info sample to ensure no hidden JSON columns with meal data
    console.log("Sampling school_info...");
    const res = await fetch(`${url}/rest/v1/school_info?limit=1`, {
        headers: {
            'apikey': serviceKey,
            'Authorization': `Bearer ${serviceKey}`,
            'Accept-Profile': 'toss',
            'Accept': 'application/json'
        }
    });
    if (res.ok) {
        console.log(await res.json());
    } else {
        console.error("Failed:", await res.text());
    }
}

main();
