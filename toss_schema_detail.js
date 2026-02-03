const serviceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImloZW56dnl4bWxxbWZyd2pla25kIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMDI5OSwiZXhwIjoyMDc2MzA2Mjk5fQ.RutW3PGpnmT_slk9BDZGwqcfE9GghBM05wCjiEIYFkQ';
const url = 'https://ihenzvyxmlqmfrwjeknd.supabase.co';

async function main() {
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

            if (data.definitions) {
                console.log("--- Schema Detail: toss ---");
                Object.keys(data.definitions).forEach(tableName => {
                    console.log(`\n[Table] ${tableName}`);
                    const props = data.definitions[tableName].properties;
                    if (props) {
                        Object.keys(props).forEach(colName => {
                            const colParam = props[colName];
                            // format usually holds the specific type like 'int4', 'uuid', etc.
                            // type holds 'string', 'integer', etc.
                            const typeInfo = colParam.format || colParam.type;
                            const desc = colParam.description ? ` - ${colParam.description}` : '';
                            console.log(`  - ${colName} (${typeInfo})${desc}`);
                        });
                    }

                    // Check required fields if listed
                    if (data.definitions[tableName].required) {
                        console.log(`  * Required: ${data.definitions[tableName].required.join(', ')}`);
                    }
                });
            } else {
                console.log("No definitions found in response.", data);
            }
        } else {
            console.error("Failed to fetch schema details:", await res.text());
        }
    } catch (e) {
        console.error("Error:", e);
    }
}

main();
