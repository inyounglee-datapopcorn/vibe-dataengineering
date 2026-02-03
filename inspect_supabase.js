const token = 'sbp_e04859cf0674add90bbd5c64ece9aecc4377ed6d';

async function main() {
    try {
        // 1. List Projects
        console.log('Fetching projects...');
        const projectsRes = await fetch('https://api.supabase.com/v1/projects', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!projectsRes.ok) {
            console.error('Failed to list projects:', await projectsRes.text());
            return;
        }

        const projects = await projectsRes.json();
        console.log(`Found ${projects.length} accessible projects.`);

        if (projects.length === 0) {
            console.log("No projects found.");
            return;
        }

        // Try to find the first likely active project
        const project = projects[0];
        console.log(`Speculated Active Project: ${project.name} (Ref: ${project.ref})`);

        // 2. Query Tables
        // Querying information_schema to get user tables
        const sql = `
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      ORDER BY table_name;
    `;

        console.log('Querying table structure...');
        const queryRes = await fetch(`https://api.supabase.com/v1/projects/${project.ref}/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: sql })
        });

        if (!queryRes.ok) {
            // sometimes 502/500 if the database is paused
            console.error('Failed to query tables. The database might be paused or inaccessible.');
            console.error('Error:', await queryRes.text());
            return;
        }

        const rows = await queryRes.json();
        console.log('\n--- Public Tables ---');
        if (Array.isArray(rows)) {
            rows.forEach(r => console.log(`- ${r.table_name}`));
        } else {
            console.log('Unexpected response format:', rows);
        }

        // 3. Get detailed columns for each table
        console.log('\n--- Detailed Schema ---');
        const msg = "Querying columns...";
        const detailSql = `
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    `;

        const detailRes = await fetch(`https://api.supabase.com/v1/projects/${project.ref}/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: detailSql })
        });

        if (detailRes.ok) {
            const details = await detailRes.json();
            // Group by table
            const tables = {};
            details.forEach(d => {
                if (!tables[d.table_name]) tables[d.table_name] = [];
                tables[d.table_name].push(d);
            });

            for (const [tName, cols] of Object.entries(tables)) {
                console.log(`\nTable: ${tName}`);
                cols.forEach(c => console.log(`  - ${c.column_name} (${c.data_type}) ${c.is_nullable === 'YES' ? 'NULL' : 'NOT NULL'}`));
            }
        }


    } catch (error) {
        console.error('Runtime Error:', error);
    }
}

main();
