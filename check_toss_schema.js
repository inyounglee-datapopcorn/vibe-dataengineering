const sbpToken = 'sbp_e04859cf0674add90bbd5c64ece9aecc4377ed6d';
const projectRef = 'ihenzvyxmlqmfrwjeknd';
const serviceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImloZW56dnl4bWxxbWZyd2pla25kIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMDI5OSwiZXhwIjoyMDc2MzA2Mjk5fQ.RutW3PGpnmT_slk9BDZGwqcfE9GghBM05wCjiEIYFkQ';
const url = 'https://ihenzvyxmlqmfrwjeknd.supabase.co';

async function main() {
    console.log("Attempt 1: Management API Query (SQL) for 'toss' schema");
    const sql = `
      SELECT table_name, column_name, data_type 
      FROM information_schema.columns 
      WHERE table_schema = 'toss' 
      ORDER BY table_name, ordinal_position;
    `;

    try {
        const res = await fetch(`https://api.supabase.com/v1/projects/${projectRef}/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${sbpToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: sql })
        });

        if (res.ok) {
            const rows = await res.json();
            if (rows.length === 0) {
                console.log("No tables found in 'toss' schema via SQL.");
            } else {
                console.log("SQL Found tables:");
                const tables = {};
                rows.forEach(r => {
                    if (!tables[r.table_name]) tables[r.table_name] = [];
                    tables[r.table_name].push(`${r.column_name} (${r.data_type})`);
                });
                for (const [t, cols] of Object.entries(tables)) {
                    console.log(`\nTable: ${t}`);
                    cols.forEach(c => console.log(`  - ${c}`));
                }
                return; // Success, stop here
            }
        } else {
            console.log("Management API failed:", await res.text());
        }
    } catch (e) { console.error("SQL Attempt Error:", e); }

    console.log("\nAttempt 2: PostgREST API with Accept-Profile: toss");
    try {
        const res = await fetch(`${url}/rest/v1/`, {
            headers: {
                'apikey': serviceKey,
                'Authorization': `Bearer ${serviceKey}`,
                'Accept-Profile': 'toss',
                'Accept': 'application/json'
            }
        });
        if (res.ok) {
            const data = await res.json();
            // If Swagger/OpenAPI
            if (data.definitions) {
                console.log("Found definitions via REST:");
                Object.keys(data.definitions).forEach(t => console.log(`- ${t}`));
            } else if (data.paths) {
                console.log("Found paths via REST:");
                Object.keys(data.paths).forEach(p => console.log(`- ${p}`));
            } else {
                console.log("REST Response:", data);
            }
        } else {
            console.log("REST API failed:", await res.text());
        }
    } catch (e) { console.error("REST Attempt Error:", e); }
}

main();
