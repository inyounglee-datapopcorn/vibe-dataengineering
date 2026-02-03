const url = 'https://ihenzvyxmlqmfrwjeknd.supabase.co';
const key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImloZW56dnl4bWxxbWZyd2pla25kIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMDI5OSwiZXhwIjoyMDc2MzA2Mjk5fQ.RutW3PGpnmT_slk9BDZGwqcfE9GghBM05wCjiEIYFkQ';

async function main() {
    try {
        console.log(`Connecting to ${url}...`);

        // 1. Get the OpenAPI definition to understand the schema
        const response = await fetch(`${url}/rest/v1/`, {
            method: 'GET',
            headers: {
                'apikey': key,
                'Authorization': `Bearer ${key}`,
                'Accept': 'application/json' // Requesting the root often lists resources or openapi
                // Note: Supabase often returns the OpenAPI spec at /rest/v1/?apikey=... but let's try basic root
            }
        });

        if (!response.ok) {
            console.error('Failed to fetch schema:', response.status, await response.text());
            return;
        }

        const data = await response.json();

        // The root of PostgREST generates an OpenAPI document if configured, or a list of paths
        // Supabase usually returns a JSON object where keys are table names (definitions) if it is swagger/openapi
        // Or it might be a map of "definitions".

        console.log('--- Tables Found ---');
        // If it's a Swagger/OpenAPI doc
        if (data.definitions) {
            Object.keys(data.definitions).forEach(tableName => {
                console.log(`\nTable: ${tableName}`);
                const props = data.definitions[tableName].properties;
                if (props) {
                    Object.keys(props).forEach(col => {
                        const info = props[col];
                        console.log(`  - ${col} (${info.type || info.format})`);
                    });
                }
            });
        } else {
            // Fallback: It might just be a list of paths if not in OpenAPI mode?
            // Actually, Supabase root often is just the index.
            console.log("Raw response structure keys:", Object.keys(data));
            if (data.paths) {
                console.log("Found paths (tables):");
                Object.keys(data.paths).filter(p => p !== '/').forEach(p => {
                    console.log(` - ${p.replace('/', '')}`);
                });
            }
        }

    } catch (err) {
        console.error(err);
    }
}

main();
