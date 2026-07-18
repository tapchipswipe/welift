process.env.PRISMA_CLI_TELEMETRY_OPTOUT = '1';
process.env.PRISMA_TELEMETRY_OPTOUT = '1';
process.env.CHECKPOINT_DISABLE = '1';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const schemaPath = path.join(__dirname, 'schema.prisma');
let schema = fs.readFileSync(schemaPath, 'utf8');

const databaseUrl = process.env.DATABASE_URL || '';
const isPostgres = databaseUrl.startsWith('postgres://') || databaseUrl.startsWith('postgresql://');

let updatedSchema = schema;
if (isPostgres) {
  console.log('Prisma Prepare DB: Detected PostgreSQL database URL.');
  // Replace datasource provider and url
  updatedSchema = schema.replace(
    /datasource\s+db\s*{[\s\S]*?}/,
    `datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}`
  );
} else {
  console.log('Prisma Prepare DB: Using SQLite database.');
  updatedSchema = schema.replace(
    /datasource\s+db\s*{[\s\S]*?}/,
    `datasource db {
  provider = "sqlite"
  url      = "file:../../data/welift.db"
}`
  );
}

if (updatedSchema !== schema) {
  fs.writeFileSync(schemaPath, updatedSchema, 'utf8');
  console.log('Prisma Prepare DB: Updated schema.prisma with correct database provider.');
} else {
  console.log('Prisma Prepare DB: schema.prisma is already up-to-date.');
}

// Generate the Prisma client
const prismaBin = path.join(__dirname, '..', 'node_modules', '.bin', 'prisma');

try {
  console.log('Prisma Prepare DB: Generating Prisma Client...');
  execSync(`"${prismaBin}" generate`, { stdio: 'inherit', env: { ...process.env, CHECKPOINT_DISABLE: '1' } });
} catch (error) {
  console.error('Prisma Prepare DB: Failed to generate Prisma Client:', error.message);
  process.exit(1);
}

// Push schema changes if using PostgreSQL
if (isPostgres) {
  try {
    console.log('Prisma Prepare DB: Pushing schema to PostgreSQL database...');
    execSync(`"${prismaBin}" db push --accept-data-loss`, { stdio: 'inherit', env: { ...process.env, CHECKPOINT_DISABLE: '1' } });
    console.log('Prisma Prepare DB: Database schema push completed.');
  } catch (error) {
    console.error('Prisma Prepare DB: Database schema push failed:', error.message);
    // Do not fail the build if the database is temporarily unreachable, but warn clearly.
    // In production/deployment settings, the DB must be reachable.
  }
}
