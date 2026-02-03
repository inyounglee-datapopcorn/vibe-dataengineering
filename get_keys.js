const token = 'sbp_e04859cf0674add90bbd5c64ece9aecc4377ed6d';
const projectRef = 'ihenzvyxmlqmfrwjeknd'; // Found in previous step

async function main() {
    try {
        console.log(`Fetching API keys for project ${projectRef}...`);
        const res = await fetch(`https://api.supabase.com/v1/projects/${projectRef}/api-keys`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) {
            console.error('Failed to get keys:', await res.text());
            return;
        }

        const keys = await res.json();
        console.log('\n--- Project API Keys ---');
        keys.forEach(k => {
            console.log(`- Name: ${k.name}`);
            console.log(`  Key: ${k.api_key}`);
        });

        // Also get basic config to see region/etc if needed
        const configRes = await fetch(`https://api.supabase.com/v1/projects/${projectRef}/config/database/pooler`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        // Just logging keys is the main goal.

    } catch (error) {
        console.error(error);
    }
}

main();
